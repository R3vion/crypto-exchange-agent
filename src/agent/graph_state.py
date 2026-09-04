from typing import TypedDict

from src.agent.state import QueryAnalysis


class AgentState(TypedDict):
    question: str

    query_analysis: QueryAnalysis

    retrieved_documents: list[dict]
    coverage_score: float | None
    rag_iterations: int | None

    tool_results: list[dict]

    risk_evidence: dict
    risk_scores: dict[str, dict]

    evidence_summary: str
    evidence_sufficient: bool

    final_answer: str