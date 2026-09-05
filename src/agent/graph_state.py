from typing import TypedDict

from src.agent.state import QueryAnalysis


class AgentState(TypedDict):
    question: str
    query_analysis: QueryAnalysis
    retrieved_documents: list[dict]
    tool_results: list[dict]

    coverage_score: float | None # not used
    rag_iterations: int | None # not used
    risk_evidence: dict # not used
    risk_scores: dict[str, dict] # not used

    evidence_summary: str
    evidence_sufficient: bool
    final_answer: str