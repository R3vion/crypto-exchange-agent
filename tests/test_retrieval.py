from src.rag.retriever import retrieve


def test_retrieval_returns_results():
    results = retrieve(
        "What is MiCA?"
    )

    assert results
    assert len(results) <= 5

    for result in results:
        assert result["text"]
        assert "score" in result
        assert "metadata" in result