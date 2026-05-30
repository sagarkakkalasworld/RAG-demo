from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langchain_community.document_loaders import TextLoader
import os

docs = []

for file in os.listdir("./incidents"):
    if file.endswith(".md"):
        loader = TextLoader(f"./incidents/{file}")
        docs.extend(loader.load())

headers = [
    ("#", "title"),
    ("##", "section")
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers
)

chunks = []

for doc in docs:
    chunks.extend(
        splitter.split_text(doc.page_content)
    )

print(f"Total Chunks: {len(chunks)}")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Vector DB created successfully")

print(f"Loaded documents: {len(docs)}")

for doc in docs:
    print(doc.metadata)