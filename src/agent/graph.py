from langgraph.graph import END, START, StateGraph

from src.agent.graph_state import AgentState
from src.agent.nodes import (
    query_analyzer_node,
    rag_node,
    route_after_rag,
    route_query,
)
from src.tools.nodes import calculator_node, risk_scoring_node


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
            "general": END,
        },
    )

    graph.add_conditional_edges(
        "rag",
        route_after_rag,
        {
            "calculator": "calculator",
            "risk_scoring": "risk_scoring",
            "complete": END,
        },
    )

    graph.add_edge(
        "calculator",
        END,
    )

    graph.add_edge(
        "risk_scoring",
        END,
    )

    return graph.compile()