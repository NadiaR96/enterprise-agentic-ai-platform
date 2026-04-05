# agents/evaluator_agent.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Evaluate if the answer is supported by the documents."),
    ("human", """Documents:\n{docs}\nAnswer:\n{answer}\nReturn a number between 0 (not supported) and 1 (fully supported).""")
])

def evaluator_agent(answer: str, docs: str) -> float:
    response = llm.invoke(prompt.format_messages(answer=answer, docs=docs))
    try:
        return float(response.content.strip())
    except:
        return 0.0