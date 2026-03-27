from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict evaluator checking if an answer is grounded in provided documents."),
    ("human", "Documents:\n{docs}\n\nAnswer:\n{answer}\n\nIs the answer supported? Reply YES or NO.")
])

def run_evaluator(answer: str, docs: str):
    response = llm.invoke(prompt.format_messages(answer=answer, docs=docs))
    return "yes" in response.content.lower()