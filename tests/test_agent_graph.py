from src.agent.graph import build_graph


def test_graph_routes_comparison():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": (
                "Which exchange is the best "
                "under MiCA?"
            )
        }
    )

    analysis = result["query_analysis"]

    assert analysis.operation == (
        "retrieve_and_compare"
    )


def test_graph_routes_risk():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": (
                "Which exchange is the riskiest "
                "and why?"
            )
        }
    )

    analysis = result["query_analysis"]

    assert analysis.operation == "risk_score"

def test_comparison_routes_to_rag():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": (
                "Which exchange is the best long-term choice "
                "under MiCA: Coinbase, Kraken or Bitpanda?"
            )
        }
    )

    assert result["query_analysis"].operation == "retrieve_and_compare"
    assert "retrieved_documents" in result
    assert len(result["retrieved_documents"]) > 0


def test_risk_question_is_analyzed():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": "Which exchange is the riskiest and why?"
        }
    )

    assert result["query_analysis"].operation == "risk_score"


def test_fee_calculation_routes_through_rag():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": (
                "How much would I pay in fees for a "
                "$10,000 Coinbase trade?"
            )
        }
    )

    assert result["query_analysis"].operation == "calculate"
    assert result["query_analysis"].calculation_amount == 10000
    assert len(result["retrieved_documents"]) > 0
    assert len(result["tool_results"]) > 0

    calculator_result = result["tool_results"][0]["result"]

    assert calculator_result["amount"] == 10000
    assert calculator_result["fee"] >= 0
    assert calculator_result["total"] >= 10000


def test_risk_question_runs_risk_tool():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": (
                "Which exchange is the riskiest and why?"
            )
        }
    )

    assert result["query_analysis"].operation == "risk_score"
    assert len(result["retrieved_documents"]) > 0
    assert len(result["tool_results"]) > 0

    tool_result = result["tool_results"][0]

    assert tool_result["tool"] == "risk_scoring"

    risk_result = tool_result["result"]

    assert 0 <= risk_result["risk_score"] <= 10
    assert risk_result["risk_level"] in {
        "low",
        "medium",
        "high",
    }


def test_end_to_end_rag_question():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": (
                # "kraken or coinbase? which exchange has the lowest risk to hold asset on?"
                # "1+1 equals? answer in whole sentence"
                "What MiCA authorization does Coinbase have in the European Union?"
            )
        }
    )

    print(result)

    assert "query_analysis" in result
    assert "retrieved_documents" in result
    assert "evidence_summary" in result
    assert "final_answer" in result

    assert len(result["retrieved_documents"]) > 0
    assert len(result["final_answer"]) > 0


def test_end_to_end_guardrails():
    graph = build_graph()

    result = graph.invoke(
        {
            "question": (
                "Which exchange is the riskiest and why?"
            )
        }
    )

    assert "final_answer" in result
    assert len(result["final_answer"]) > 0