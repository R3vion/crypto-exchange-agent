from typing import TypedDict

from src.agent.state import QueryAnalysis


class AgentState(TypedDict, total=False):
    question: str

    query_analysis: QueryAnalysis

    retrieved_documents: list[dict]

    tool_results: list[dict]

    risk_evidence: dict

    final_answer: str