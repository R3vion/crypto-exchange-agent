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