from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "Summarize the following text:\n\n{text}"
)

def summary_agent(text: str):
    chain = prompt | llm
    return chain.invoke({"text": text})