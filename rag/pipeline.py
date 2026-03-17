def retrieve(query):
    return ["docA", "docB"]

def generate_answer(query):
    docs = retrieve(query)
    return f"Answer from {docs}"
