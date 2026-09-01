from src.agent.graph_state import AgentState
from src.agent.query_analyzer import analyze_query
from src.rag.graph import build_rag_graph


def query_analyzer_node(state: AgentState) -> AgentState:
    analysis = analyze_query(state["question"])

    return {
        "query_analysis": analysis,
    }


def route_query(state: AgentState) -> str:
    analysis = state["query_analysis"]

    return analysis.operation


def rag_node(state: AgentState) -> AgentState:
    rag_graph = build_rag_graph()

    analysis = state["query_analysis"]

    result = rag_graph.invoke(
        {
            "question": state["question"],
            "exchanges": analysis.exchanges,
            "jurisdiction": analysis.jurisdiction,
        }
    )

    return {
        "retrieved_documents": result.get(
            "retrieved_documents",
            [],
        ),
    }