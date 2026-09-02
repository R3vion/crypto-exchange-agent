from src.agent.evidence import evidence_review_node


def test_evidence_review():
    result = evidence_review_node(
        {
            "question": "What MiCA authorization does Coinbase have?",
            "retrieved_documents": [
                {
                    "text": (
                        "Coinbase Luxembourg S.A. received "
                        "authorization under MiCA."
                    )
                }
            ],
            "tool_results": [],
        }
    )

    assert "evidence_summary" in result
    assert isinstance(
        result["evidence_sufficient"],
        bool,
    )