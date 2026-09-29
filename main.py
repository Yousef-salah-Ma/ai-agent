from fastapi import FastAPI, Depends , HTTPException
from pydantic import BaseModel 
from auth import register_user, login_users
from schema import reg_user , login_user
from security import get_current_user
from tools import (
    web_search,
    calculator,
    local_search,
    long_term_memory
)


from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage

from langgraph.prebuilt import ToolNode
from langgraph.graph import add_messages , START , END , StateGraph 
from langgraph.graph import MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from fastapi.responses import StreamingResponse

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key= "api_key"
)

tools = [web_search,
    calculator,
    local_search,
    long_term_memory]

llm  = llm.bind_tools(tools)

tool_node = ToolNode(tools)
def llm_node(state):
    response = llm.invoke(state["messages"])



    return {
        "messages": [response]
    }
graph = StateGraph(MessagesState)

graph.add_node("llm" , llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START , "llm")
graph.add_edge("tools", "llm")

def route(state):
    last_message = state["messages"][-1]



    if last_message.tool_calls:
        return "tools"

    return "end"


graph.add_conditional_edges("llm" ,route ,{
    "tools":"tools",
    "end":END
} )

cm = SqliteSaver.from_conn_string("test.db")

checkpointer = cm.__enter__()

model = graph.compile(
        checkpointer=checkpointer
    )


class user_in(BaseModel):
    user_input: str


app = FastAPI()

@app.post("/login")
def login(login_sch : login_user ):
    return login_users(login_sch.email , login_sch.password)

@app.post("/register")
def register(data: reg_user ):

    result = register_user(data)

    if result["message"] == "تم التسجيل بنجاح":
        return result

    raise HTTPException(
        status_code=409,
        detail=result["message"]
    )

@app.post("/chat")
def chat(
    message: user_in,
    token: str = Depends(get_current_user)
):
    
    config = {
            "configurable": {
                "thread_id": token
            }
        }
    
    res = model.invoke({"messages":HumanMessage(message.user_input)} , config)

    return {
        "response":res["messages"][-1].text,
        
    }
