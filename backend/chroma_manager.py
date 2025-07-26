import chromadb
from backend.file_ingest import embedder
from langchain_community.vectorstores import Chroma


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="user_documents")

def add_to_chroma(text_chunks, user_id: str, filename: str):
    """Embed chunks and store in ChromaDB with user metadata."""

    documents = [chunk["text"] for chunk in text_chunks]
    metadatas = [{"user_id": user_id, "filename": filename} for _ in text_chunks]
    ids = [f"{user_id}_{filename}_{i}" for i in range(len(text_chunks))]

    embeddings = embedder.embed_documents(documents)

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ Added {len(documents)} chunks to ChromaDB for user: {user_id}, file: {filename}")

def get_user_retriever(user_id: str, k: int = 4):
    """Return retriever for a given user using metadata filter."""

    return Chroma(
        client=chroma_client,
        collection_name="user_documents",
        embedding_function=embedder
    ).as_retriever(
        search_kwargs={"k": k, "filter": {"user_id": user_id}}
    )
