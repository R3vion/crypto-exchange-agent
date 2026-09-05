from src.agent.graph_state import AgentState
from src.agent.query_analyzer import analyze_query
from src.rag.graph import build_rag_graph


def query_analyzer_node(state: AgentState) -> AgentState:
    analysis = analyze_query(state["question"])
    # print("\n=== QUERY ANALYZER DEBUG ===")
    # print("question:", state["question"])
    # print("operation:", analysis.operation)
    # print("exchanges:", analysis.exchanges)
    # print("jurisdiction:", analysis.jurisdiction)
    # print("requires_risk_scoring:", analysis.requires_risk_scoring)
    # print("============================\n")

    state["query_analysis"] = analysis

    return state


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

    state["retrieved_documents"] = result.get("retrieved_documents", [])
    state["coverage_score"] = result.get("coverage_score")
    state["rag_iterations"] = result.get("iteration")

    return state

def route_after_rag(state: AgentState) -> str:
    analysis = state["query_analysis"]

    if analysis.operation == "calculate":
        return "calculator"

    if analysis.operation == "risk_score" or analysis.requires_risk_scoring:
        return "risk_scoring"

    return "complete"