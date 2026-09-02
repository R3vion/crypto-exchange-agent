from src.agent.answer_generator import answer_generator_node


def test_answer_generator():
    result = answer_generator_node(
        {
            "question": "What MiCA authorization does Coinbase have?",
            "evidence_summary": (
                "Coinbase Luxembourg S.A. received "
                "authorization under MiCA."
            ),
            "tool_results": [],
            "evidence_sufficient": True,
        }
    )

    assert "final_answer" in result
    assert len(result["final_answer"]) > 0