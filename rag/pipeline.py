def retrieve(query):
    docs = [
        "Terraform manages infrastructure",
        "RAG improves factual accuracy",
        "Agents divide tasks efficiently"
    ]

    # naive similarity
    return sorted(docs, key=lambda d: query.lower() in d.lower(), reverse=True)
def generate_answer(query):
    docs = retrieve(query)
    return f"Answer from {docs}"
