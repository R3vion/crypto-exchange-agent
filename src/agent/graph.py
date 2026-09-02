from langgraph.graph import END, START, StateGraph

from src.agent.graph_state import AgentState
from src.agent.nodes import (
    query_analyzer_node,
    rag_node,
    route_after_rag,
    route_query,
)
from src.tools.nodes import calculator_node, risk_scoring_node
from src.agent.answer_generator import answer_generator_node
from src.agent.evidence import evidence_review_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node(
        "query_analyzer",
        query_analyzer_node,
    )

    graph.add_node(
        "rag",
        rag_node,
    )

    graph.add_node(
        "calculator",
        calculator_node,
    )

    graph.add_node(
        "risk_scoring",
        risk_scoring_node,
    )

    graph.add_node(
        "evidence_review",
        evidence_review_node,
    )

    graph.add_node(
        "answer_generator",
        answer_generator_node,
    )

    graph.add_edge(
        START,
        "query_analyzer",
    )

    graph.add_conditional_edges(
        "query_analyzer",
        route_query,
        {
            "retrieve": "rag",
            "retrieve_and_compare": "rag",
            "calculate": "rag",
            "risk_score": "rag",
            "compare": "rag",
            "general": "answer_generator",
        },
    )

    graph.add_conditional_edges(
        "rag",
        route_after_rag,
        {
            "calculator": "calculator",
            "risk_scoring": "risk_scoring",
            "complete": "evidence_review",
        },
    )

    graph.add_edge(
        "calculator",
        "evidence_review",
    )

    graph.add_edge(
        "risk_scoring",
        "evidence_review",
    )

    graph.add_edge(
        "evidence_review",
        "answer_generator",
    )

    graph.add_edge(
        "answer_generator",
        END,
    )

    return graph.compile()