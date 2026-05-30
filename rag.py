from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

llm = ChatOllama(
    model="llama3"
)

while True:

    question = input("\nAsk Question: ")

    docs = db.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        [d.page_content for d in docs]
    )

    prompt = f"""
You are a DevOps incident assistant.

Use only the context below.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    print("\nAnswer:")
    print(response.content)