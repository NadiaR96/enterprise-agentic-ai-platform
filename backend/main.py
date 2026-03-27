from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COST_THRESHOLD = float(os.getenv("COST_THRESHOLD", 10))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.7))

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in .env")

from agents.qa_agent import answer_question
from agents.summary_agent import summarize_docs
from agents.planner_agent import plan_query
from agents.evaluator_agent import evaluate_response
from rag.pipeline import retrieve, detect_hallucination

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Multi-user memory with logs
memory = {}

@app.get("/query")
def query(q: str, user_id: str = "demo_user"):
    if user_id not in memory:
        memory[user_id] = []

    # Planner decides which agents to use
    agents_to_use = plan_query(q)

    # Retrieve top documents
    docs = retrieve(q, top_k=3)

    responses = []
    logs = {
        "planner": agents_to_use,
        "retrieved_docs": docs,
        "cost": 0,
        "agent_confidences": {}
    }

    # Execute agents with cost & confidence checks
    for agent_name in agents_to_use:
        if logs["cost"] > COST_THRESHOLD:
            logs[f"{agent_name}_skipped"] = "Cost threshold reached"
            continue

        if agent_name == "qa":
            resp, cost, confidence = answer_question(q)
        elif agent_name == "summary":
            resp, cost, confidence = summarize_docs(docs)
        else:
            continue

        logs["cost"] += cost
        logs["agent_confidences"][agent_name] = confidence

        if confidence < CONFIDENCE_THRESHOLD:
            logs[f"{agent_name}_skipped"] = "Confidence too low"
            continue

        responses.append(resp)
        logs[agent_name] = resp

    combined_response = " | ".join(responses)

    # Evaluate final response for hallucinations
    if detect_hallucination(combined_response, docs):
        combined_response = evaluate_response(combined_response, docs)
        logs["evaluation"] = combined_response

    memory[user_id].append({
        "query": q,
        "response": combined_response,
        "logs": logs
    })

    return {
        "user_id": user_id,
        "response": combined_response,
        "history": memory[user_id]
    }