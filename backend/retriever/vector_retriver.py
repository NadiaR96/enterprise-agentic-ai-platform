from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Sample knowledge base
documents = [
    "Terraform manages infrastructure",
    "RAG improves factual accuracy",
    "Agents divide tasks efficiently"
]

splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=10)
chunks = [chunk for doc in documents for chunk in splitter.split_text(doc)]
vector_store = FAISS.from_texts(chunks, OpenAIEmbeddings())

memory = {}

def retrieve(query: str, user_id: str = None, k: int = 3):
    docs = vector_store.similarity_search(query, k=k)
    if user_id:
        seen = memory.get(user_id, [])
        docs = [d for d in docs if d.page_content not in seen]
        memory.setdefault(user_id, []).extend([d.page_content for d in docs])
    return docs