from src.rag.graph import build_rag_graph

def test_rag_graph_returns_documents():
    graph = build_rag_graph()

    result = graph.invoke(
        {
            "question": (
                "What MiCA authorization does Coinbase have "
                "in the European Union?"
            ),
            "exchanges": ["Coinbase"],
            "jurisdiction": "EU",
        }
    )

    assert "retrieved_documents" in result
    assert len(result["retrieved_documents"]) > 0
    assert result["iteration"] <= 3
    assert 0.4 <= result["coverage_score"] <= 1.0