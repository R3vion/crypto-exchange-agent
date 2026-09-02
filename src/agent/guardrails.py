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

    violations = [
        pattern
        for pattern in FORBIDDEN_PATTERNS
        if pattern in normalized_answer
    ]

    if violations:
        safe_answer = (
            "I cannot provide personalized investment advice "
            "or guarantee financial returns. "
            "The available evidence can only be used for "
            "general research and comparison."
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        )

        return {
            "final_answer": f"{answer}\n\n{'!'*50}\n{safe_answer.upper()}\n{'!'*50}", 
            # showing the original answer as well since it is only a PoK (Proof of Knowledge ;)
            # but dont use this tool as a financial advisor pls.
        }

    return {
        "final_answer": answer,
    }