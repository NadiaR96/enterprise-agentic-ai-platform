prompt = ChatPromptTemplate.from_messages([
    ("system", "You summarize answers concisely."),
    ("human", "Summarize:\n{answers}")
])