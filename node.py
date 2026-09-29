from langchain_core.prompts import ChatPromptTemplate
from tools import (
    web_search,
    calculator,
    local_search,
    long_term_memory
)
from langchain_google_genai import ChatGoogleGenerativeAI

import os



llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

tools = [web_search,
    calculator,
    local_search,
    long_term_memory]

llm  = llm.bind_tools(tools)

prompt = ChatPromptTemplate.from_messages([
    ("system" , "ساعدني انت شغال  مساعد معايا ") ,
    ("human" , """
    User input:
    {user_input}
    
    Tool result:
    {result_tool}
    """)
])

def llm_node(state):

    chain = prompt | llm

    res = chain.invoke({
        "user_input": state.user_input,
        "result_tool": state.result_tool
    })

    if res.tool_calls:
        return {
            "route": res.tool_calls[0]["name"],
            "args": res.tool_calls[0]["args"]
        }

    else:
        return {
            "route": "direct",
            "result_model": res.content[0]["text"]
        }

def web_search_node(state):

    res = web_search.invoke(state.args["question"])
    return {"result_tool": res}

def calculator_node(state):
    res = calculator.invoke(**state.args)

    return {
        "result_tool": res
    }

def long_term_memory_node(state):

    res = long_term_memory.invoke(state.args["query"])

    return {
        "result_tool": res
    }

def local_search_node(state):
    res = local_search.invoke(state.args["query"])

    return {
        "result_tool": res
    }