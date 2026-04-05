# backend/utils.py
import random

def track_cost(agent_func, input_data):
    """
    Simulate tracking the cost of running an agent.
    """
    response = agent_func(input_data)
    cost = random.uniform(0.01, 0.1)  # Simulated cost for now
    return response, cost

def detect_hallucination(response: str, docs: str) -> bool:
    """
    Simple hallucination detector: returns True if none of the document content appears in the response.
    """
    return not any(sentence.strip() in response for sentence in docs.splitlines() if sentence.strip())