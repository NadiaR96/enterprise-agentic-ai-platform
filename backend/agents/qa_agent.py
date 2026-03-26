import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from rag.pipeline import generate_answer

def qa_agent(query):
    return generate_answer(query)
