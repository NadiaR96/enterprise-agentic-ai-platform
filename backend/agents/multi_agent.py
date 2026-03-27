from .planner_agent import run_planner
from .qa_agent import run_qa
from .summary_agent import run_summary
from .evaluator_agent import run_evaluator

MAX_RETRIES = 2

def run_pipeline(query: str, user_id: str = "demo_user"):

    plan = run_planner(query)

    attempts = 0
    is_valid = False
    answer = ""
    docs = ""

    while attempts <= MAX_RETRIES and not is_valid:
        answer, docs = run_qa(query, user_id, retry=(attempts > 0))
        is_valid = run_evaluator(answer, docs)

        if not is_valid:
            attempts += 1

    # fallback if still failing
    if not is_valid:
        answer = "I'm not confident enough to answer this based on available documents."

    summary = run_summary([answer])

    return {
        "plan": plan,
        "qa_answer": answer,
        "summary": summary,
        "validated": is_valid,
        "attempts": attempts
    }