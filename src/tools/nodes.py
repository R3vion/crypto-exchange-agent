from src.agent.graph_state import AgentState
from src.tools.calculator import calculate_fee
from src.tools.fee_extractor import extract_fee_rate


def calculator_node(state: AgentState) -> AgentState:
    analysis = state["query_analysis"]

    if analysis.calculation_amount is None:
        raise ValueError(
            "Calculator requires a calculation amount."
        )

    documents = state.get("retrieved_documents", [])

    if not documents:
        raise ValueError(
            "Calculator requires retrieved evidence."
        )

    fee_rate = None
    fee_source = None

    for document in documents:
        text = document.get("text", "")

        extracted_rate = extract_fee_rate(text)

        if extracted_rate is not None:
            fee_rate = extracted_rate
            fee_source = document
            break

    if fee_rate is None:
        raise ValueError(
            "Could not extract a fee rate from retrieved evidence."
        )

    result = calculate_fee(
        amount=analysis.calculation_amount,
        fee_rate=fee_rate,
    )

    return {
        "tool_results": [
            {
                "tool": "calculator",
                "result": result,
                "source": fee_source,
            }
        ]
    }