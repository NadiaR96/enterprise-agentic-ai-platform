from agents.qa_agent import qa_agent
from agents.summary_agent import summary_agent

def route_query(query):
    if "summary" in query:
        return summary_agent(query)
    return qa_agent(query)
