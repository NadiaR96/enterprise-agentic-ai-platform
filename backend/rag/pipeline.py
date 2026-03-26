def retrieve(query):
    docs = [
        "Terraform manages infrastructure",
        "RAG improves factual accuracy",
        "Agents divide tasks efficiently"
    ]

    # naive similarity
    return sorted(docs, key=lambda d: query.lower() in d.lower(), reverse=True)

def detect_hallucination(response, docs):
    if not any(doc in response for doc in docs):
        return True
    return False
def generate_answer(query):
    docs = retrieve(query)
    response = f"Answer from {docs}"
    if detect_hallucination(response, docs):
        return "I'm sorry, but I'm not sure about that."
    return response
