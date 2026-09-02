from langchain_ollama import ChatOllama

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def create_llm() -> ChatOllama:
    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.0,
        reasoning=False,
        base_url=OLLAMA_BASE_URL,
    )