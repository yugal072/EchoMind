from app.RAG.index import contextual_prompt, llm
chain = contextual_prompt | llm
result = chain.invoke({"input": "what is in my obsidian vault", "chat_history": []})
print(repr(result.content))