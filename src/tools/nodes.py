from src.agent.graph_state import AgentState
from src.tools.calculator import calculate_fee
from src.tools.fee_extractor import extract_fee_rate
from src.tools.risk_evaluator import evaluate_risk_evidence
from src.tools.risk_scoring import RiskFactors, calculate_risk_score


def risk_scoring_node(state: AgentState) -> AgentState:
    question = state["question"]
    analysis = state["query_analysis"]

    documents = state.get("retrieved_documents", [])
    if not documents:
        raise ValueError("Risk scoring requires retrieved evidence.")

    exchanges = analysis.exchanges

    risk_scores = {}
    tool_results = []

    for exchange in exchanges:
        exchange_documents = []
        for document in documents:
            if document.get("metadata", {}).get("exchange") == exchange:
                exchange_documents.append(document)

        if len(exchange_documents):
            raise ValueError(f"No retrieved evidence found for exchange: {exchange}")

        evaluation = evaluate_risk_evidence(question=question, documents=exchange_documents)

        factors = RiskFactors(
            regulatory_risk=evaluation.regulatory_risk,
            security_risk=evaluation.security_risk,
            transparency_risk=evaluation.transparency_risk,
            operational_risk=evaluation.operational_risk
        )

        score = calculate_risk_score(factors)

        risk_scores[exchange] = {
            "score": score,
            "regulatory_risk": evaluation.regulatory_risk,
            "security_risk": evaluation.security_risk,
            "transparency_risk": evaluation.transparency_risk,
            "operational_risk": evaluation.operational_risk,
            "reasoning": evaluation.reasoning,
        }

        tool_results.append(
            {
                "tool": "risk_scoring",
                "exchange": exchange,
                "result": score,
                "reasoning": evaluation.reasoning,
            }
        )

    return {
        "risk_scores": risk_scores,
        "tool_results": tool_results,
    }

def calculator_node(state: AgentState) -> AgentState:
    analysis = state["query_analysis"]

    if analysis.calculation_amount is None:
        raise ValueError("Calculator requires a calculation amount.")

    documents = state.get("retrieved_documents", [])
    if not documents:
        raise ValueError("Calculator requires retrieved evidence.")

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
        raise ValueError("Could not extract a fee rate from retrieved evidence.")

    result = calculate_fee(amount=analysis.calculation_amount, fee_rate=fee_rate)

    return {
        "tool_results": [
            {
                "tool": "calculator",
                "result": result,
                "source": fee_source,
            }
        ]
    }