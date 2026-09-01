from langgraph.graph import END, START, StateGraph

from src.agent.graph_state import AgentState
from src.agent.nodes import (
    query_analyzer_node,
    rag_node,
    route_query,
)


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
            "calculate": END,
            "risk_score": END,
            "compare": END,
            "general": END,
        },
    )

    graph.add_edge(
        "rag",
        END,
    )

    return graph.compile()