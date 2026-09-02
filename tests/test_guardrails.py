from src.agent.guardrails import guardrails_node


def test_guardrails_allow_normal_answer():
    result = guardrails_node(
        {
            "final_answer": (
                "Coinbase has received MiCA authorization "
                "through its Luxembourg entity."
            )
        }
    )

    assert "I cannot provide personalized investment advice".upper() not in result["final_answer"]


def test_guardrails_block_financial_advice():
    result = guardrails_node(
        {
            "final_answer": (
                "You should invest in Coinbase because "
                "it has guaranteed profit."
            )
        }
    )

    assert "I cannot provide personalized investment advice".upper() in result["final_answer"]