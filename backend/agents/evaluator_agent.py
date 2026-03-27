from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..retriever.vector_retriever import retrieve

llm = ChatOpenAI(temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY using provided documents. If unsure, say you don't know."),
    ("human", "Documents:\n{docs}\n\nQuestion: {query}")
])

def run_qa(query: str, user_id: str = None):
    docs = retrieve(query, user_id)
    doc_text = "\n".join([d.page_content for d in docs])

    response = llm.invoke(prompt.format_messages(query=query, docs=doc_text))

    return response.content, doc_text