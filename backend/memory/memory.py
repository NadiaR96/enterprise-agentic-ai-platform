memory = {}

def add_entry(user_id: str, data: dict):
    if user_id not in memory:
        memory[user_id] = []
    memory[user_id].append(data)

def get_history(user_id: str):
    return memory.get(user_id, [])