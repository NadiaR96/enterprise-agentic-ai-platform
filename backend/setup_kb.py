# backend/setup_kb.py
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import os
import pickle

kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base/example_docs")
vector_file = os.path.join(os.path.dirname(__file__), "knowledge_base/faiss_index.pkl")

all_docs = []

for filename in os.listdir(kb_path):
    path = os.path.join(kb_path, filename)
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(path)
        all_docs.extend(loader.load())
    elif filename.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            all_docs.append({"page_content": f.read()})

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = [chunk for doc in all_docs for chunk in splitter.split_text(doc["page_content"])]

vector_store = FAISS.from_texts(chunks, OpenAIEmbeddings())

# Save the vector store for later
with open(vector_file, "wb") as f:
    pickle.dump(vector_store, f)

print(f"Knowledge base initialized with {len(chunks)} chunks and saved to {vector_file}")