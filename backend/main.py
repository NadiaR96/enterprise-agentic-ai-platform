from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator.orchestrator import route_query

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # adjust port if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory per-user history
memory = {}

# Request model
class QueryRequest(BaseModel):
    q: str
    user_id: str = "demo_user"

@app.post("/query")
def query(request: QueryRequest):
    user_id = request.user_id
    q = request.q

    if user_id not in memory:
        memory[user_id] = []

    response = route_query(q)  # call your orchestrator

    memory[user_id].append({
        "query": q,
        "response": response
    })

    return {
        "user_id": user_id,
        "response": response,
        "history": memory[user_id]
    }