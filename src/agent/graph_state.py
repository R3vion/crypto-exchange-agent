from typing import TypedDict

from src.agent.state import QueryAnalysis


class AgentState(TypedDict, total=False):
    question: str

    query_analysis: QueryAnalysis

    retrieved_documents: list[dict]

    tool_results: list[dict]

    risk_evidence: dict
    risk_scores: dict[str, dict]

    evidence_summary: str
    evidence_sufficient: bool

    final_answer: str