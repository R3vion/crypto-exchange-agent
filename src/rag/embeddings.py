from langchain_ollama import OllamaEmbeddings

from src.config import OLLAMA_BASE_URL


EMBEDDING_MODEL = "nomic-embed-text"


def create_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL,
    )