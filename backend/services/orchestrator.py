# orchestrator.py
try:
    from backend.agents.planner_agent import planner_agent
    from backend.agents.qa_agent import answer as qa_agent
    from backend.agents.summary_agent import summary_agent
    from backend.agents.evaluator_agent import evaluator_agent
except ModuleNotFoundError:
    from agents.planner_agent import planner_agent
    from agents.qa_agent import answer as qa_agent
    from agents.summary_agent import summary_agent
    from agents.evaluator_agent import evaluator_agent

CONFIDENCE_THRESHOLD = 0.7

def route_query(query: str):
    flow = planner_agent(query)

    if flow == "summary":
        # minimal LLM call: just summarize cached content
        docs = ["Cached responses or docs..."]  # Replace with memory if you add
        answer = summary_agent("\n\n".join(docs))
        confidence = 1.0
    else:
        # full QA flow
        answer = qa_agent(query)
        doc_text = ""
        confidence = evaluator_agent(answer, doc_text)

    grounded = confidence >= CONFIDENCE_THRESHOLD

    return {
        "answer": answer,
        "confidence": confidence,
        "grounded": grounded,
        "retry_used": False
    }