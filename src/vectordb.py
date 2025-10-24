# src/chroma.py
import chromadb
from chromadb.utils import embedding_functions
from src.config import settings
import os

chroma_client = None
collection = None
embedding_func = None

def get_embedding_func():
    global embedding_func
    if embedding_func is None:
        print("🧠 Loading SentenceTransformer model (once)...")
        embedding_func = embedding_functions.CohereEmbeddingFunction(
            api_key=settings.COHERE_API_KEY,
            model_name="embed-multilingual-v3.0"
        )
    return embedding_func

def init_chroma():
    global chroma_client, collection
    os.makedirs(settings.CHROMA_PERSIST_PATH, exist_ok=True)

    if chroma_client is None:
        chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_PATH)

    if collection is None:
        collection = chroma_client.get_or_create_collection(
            name="reference_docs",
            embedding_function=get_embedding_func()
        )
    print("✅ ChromaDB initialized.")
    return chroma_client, collection


def get_chroma_collection():
    global collection
    if collection is None:
        init_chroma()
    return collection
