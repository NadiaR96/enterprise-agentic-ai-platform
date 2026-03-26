import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI
from orchestrator.orchestrator import route_query

app = FastAPI()

memory = {}

@app.get("/query")
def query(q: str, user_id: str = "demo_user"):
    if user_id not in memory:
        memory[user_id] = []

    response = route_query(q)

    memory[user_id].append({
        "query": q,
        "response": response
    })

    return {
        "user_id": user_id,
        "response": response,
        "history": memory[user_id]
    }