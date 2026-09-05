from src.agent.graph_state import AgentState


FORBIDDEN_PATTERNS = [
    "guaranteed profit",
    "guaranteed return",
    "risk-free investment",
    "you should invest",
    "you must invest",
]


def guardrails_node(state: AgentState) -> AgentState:
    answer = state.get("final_answer", "")

    normalized_answer = answer.lower()

    violation_triggered = False
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in normalized_answer:
            violation_triggered = True
            break

    if violation_triggered:
        safe_answer = (
            "I cannot provide personalized investment advice or guarantee financial returns. "
            "The available evidence can only be used for general research and comparison."
        )

        state["final_answer"] = f"{answer}\n\n{'!'*75}\n{safe_answer.upper()}\n{'!'*75}"
            # showing the original answer as well since it is only a PoK (Proof of Knowledge ;)
            # but dont use this tool as a financial advisor pls.
        
    state["final_answer"] = answer

    return state