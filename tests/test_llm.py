from src.llm import create_llm


def test_llm_connection():
    llm = create_llm()

    response = llm.invoke(
        "In one sentence, what is MiCA?"
    )

    assert response.content