from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path="backend/.env")

# Get OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in backend/.env")

# Import your orchestrator after env is loaded
from orchestrator.orchestrator import route_query
from langchain.chat_models import ChatOpenAI

# Initialize ChatOpenAI
chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")

app = FastAPI()

# Example middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory multi-user memory
memory = {}

@app.get("/query")
def query(q: str, user_id: str = "demo_user"):
    if user_id not in memory:
        memory[user_id] = []

    response = route_query(q)  # Your RAG / multi-agent logic

    memory[user_id].append({
        "query": q,
        "response": response
    })

    return {
        "user_id": user_id,
        "response": response,
        "history": memory[user_id]
    }