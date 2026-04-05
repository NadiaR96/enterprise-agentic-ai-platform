# Chat models
from langchain_openai import ChatOpenAI

# Prompt templates
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "Decide the best action for this query: {query}"
)

def planner_agent(query: str):
    chain = prompt | llm
    return chain.invoke({"query": query})