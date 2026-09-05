from typing import TypedDict


class RAGState(TypedDict):
    question: str
    exchanges: list[str]
    jurisdiction: str | None

    retrieved_documents: list[dict]

    iteration: int
    coverage_score: float
    coverage_sufficient: bool
    coverage_by_exchange: dict[str, float]
    missing_exchanges: list[str]
    retrieval_query: str