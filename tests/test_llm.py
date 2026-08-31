from src.llm import create_llm


def test_llm_connection():
    llm = create_llm()

    response = llm.invoke(
        "hii there!! be short!"
    )

    assert response.content