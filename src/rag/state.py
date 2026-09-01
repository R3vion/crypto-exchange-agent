from typing import TypedDict


class RAGState(TypedDict, total=False):
    question: str
    exchanges: list[str]
    jurisdiction: str | None

    retrieved_documents: list[dict]

    iteration: int
    coverage_score: float
    coverage_sufficient: bool
    retrieval_query: str