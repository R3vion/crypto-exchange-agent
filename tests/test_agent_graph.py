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