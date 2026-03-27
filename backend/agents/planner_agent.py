from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a planner deciding how to process a user query."),
    ("human", "Query: {query}\n\nDecide: should we retrieve documents and answer, or just summarize?")
])

def run_planner(query: str):
    response = llm.invoke(prompt.format_messages(query=query))
    return response.content.lower()