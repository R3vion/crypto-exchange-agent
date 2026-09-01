from src.agent.graph_state import AgentState
from src.agent.query_analyzer import analyze_query


def query_analyzer_node(state: AgentState) -> AgentState:
    analysis = analyze_query(
        state["question"]
    )

    return {
        "query_analysis": analysis,
    }

def route_query(state: AgentState) -> str:
    analysis = state["query_analysis"]

    return analysis.operation