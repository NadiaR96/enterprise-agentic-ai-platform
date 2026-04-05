# Minimal example using LangChain v1.2+
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

chat = ChatOpenAI(temperature=0)

def answer(query):
    prompt = ChatPromptTemplate.from_template("Answer this: {input}")
    chain = prompt | chat
    response = chain.invoke({"input": query})
    return response.content
