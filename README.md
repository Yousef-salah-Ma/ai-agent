# AI Agent API

An AI Agent API built with **FastAPI** and **LangGraph**, featuring authentication, tool calling, web search, local document search, calculator, and short-term / long-term memory.

## 🚀 Features

* FastAPI REST API
* JWT Authentication
* User Registration & Login
* Password Hashing
* LangGraph Agent
* Tool Calling
* Web Search
* Calculator
* Local Document Search using Chroma
* Long-Term Memory using FAISS
* Short-Term Memory using SQLite
* LangGraph Checkpointing
* Gemini LLM

## 🏗️ Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ├── Register / Login
  │       │
  │       └── JWT Authentication
  │
  └── /chat
        │
        ▼
    LangGraph Agent
        │
        ├── LLM
        │
        └── Tools
             ├── Web Search
             ├── Calculator
             ├── Local Search
             └── Long-Term Memory
```

## 🛠️ Tech Stack

* Python
* FastAPI
* Pydantic
* LangChain
* LangGraph
* Google Gemini
* SQLite
* Chroma
* FAISS
* JWT
* Tavily

## 📁 Project Structure

```text
AI-Agent/
│
├── main.py
├── auth.py
├── security.py
├── schema.py
├── tools.py
├── memory.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔐 Authentication

The API uses JWT authentication.

### Register

```http
POST /register
```

Creates a new user and stores the password as a hash.

### Login

```http
POST /login
```

Returns an access token:

```json
{
  "access_token": "YOUR_TOKEN",
  "token_type": "bearer"
}
```

The token is then used to access protected endpoints.

```http
Authorization: Bearer YOUR_TOKEN
```

## 💬 Chat

```http
POST /chat
```

Example request:

```json
{
  "user_input": "What is the capital of Egypt?"
}
```

The authenticated user can interact with the AI agent.

The agent can decide whether to use:

* Web Search
* Calculator
* Local Search
* Long-Term Memory

## 🧠 Memory

The project uses different types of memory.

### Short-Term Memory

LangGraph checkpointing with SQLite is used to preserve the conversation state.

### Long-Term Memory

Important information can be stored and later retrieved using vector similarity search with FAISS.

## 🔧 Tools

The agent currently has several tools:

### Web Search

Uses Tavily to search the web.

### Calculator

Performs mathematical calculations.

### Local Search

Searches local documents stored in Chroma.

### Long-Term Memory

Retrieves relevant stored memories using embeddings and FAISS.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-agent-fastapi.git
cd ai-agent-fastapi
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit the `.env` file to GitHub.

Use `.env.example` as a template.

## ▶️ Run the API

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

FastAPI Swagger UI will allow you to test the API.

## 🎯 Project Goal

The goal of this project is to build a practical AI Agent backend capable of combining:

* LLM reasoning
* Tool calling
* Retrieval
* Memory
* Authentication
* API development

This project is part of my journey toward building production-oriented AI systems and automation solutions.

## 📌 Future Improvements

* PostgreSQL
* SQLAlchemy
* Better RAG evaluation
* Streaming responses
* AI response streaming
* More advanced agent routing
* Multi-agent architecture
* Observability
* Automated testing
* Docker deployment
* Production deployment

## 👨‍💻 Author

**Yousef Saleh**

AI / Machine Learning Engineer
