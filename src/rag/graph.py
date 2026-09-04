from langgraph.graph import END, START, StateGraph

from src.rag.nodes import evaluate_coverage, retrieve_documents, route_after_coverage
from src.rag.state import RAGState


def build_rag_graph():
    graph = StateGraph(RAGState)

    # N O D E S
    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_node("evaluate_coverage", evaluate_coverage)

    # E D G E S
    graph.add_edge(START, "retrieve_documents")
    graph.add_edge("retrieve_documents","evaluate_coverage")
    graph.add_conditional_edges("evaluate_coverage", route_after_coverage,
        {
            "retrieve_again": "retrieve_documents",
            "complete": END,
        }
    )

    return graph.compile()