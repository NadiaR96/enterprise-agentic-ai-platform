from fastapi import FastAPI
from orchestrator.orchestrator import route_query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/query")
def query(q: str):
    result = route_query(q)
    return {"query": q, "response": result}
