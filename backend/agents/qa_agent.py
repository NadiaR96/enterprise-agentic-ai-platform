from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..retriever.vector_retriever import retrieve

llm = ChatOpenAI(temperature=0)

# Normal prompt
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY using provided documents."),
    ("human", "Documents:\n{docs}\n\nQuestion: {query}")
])

# Retry prompt (stricter)
retry_prompt = ChatPromptTemplate.from_messages([
    ("system", "You previously gave an incorrect or ungrounded answer. ONLY use the documents. If unsure, say 'I don't know'."),
    ("human", "Documents:\n{docs}\n\nQuestion: {query}")
])

def run_qa(query: str, user_id: str = None, retry=False):
    docs = retrieve(query, user_id)
    doc_text = "\n".join([d.page_content for d in docs])

    prompt = retry_prompt if retry else qa_prompt

    response = llm.invoke(prompt.format_messages(query=query, docs=doc_text))

    return response.content, doc_text