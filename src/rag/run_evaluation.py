from src.rag.evaluation import (
    evaluate_retrieval,
    load_questions,
)


def main() -> None:
    questions = load_questions(
        "tests/data/retrieval_questions.yaml"
    )

    evaluation = evaluate_retrieval(
        questions,
        top_k=5,
    )

    # print()
    # print("Retrieval Evaluation")
    # print("=====================")
    # print(f"Questions: {evaluation['total']}")
    # print(f"Hits:      {evaluation['hits']}")
    # print(f"Hit rate:  {evaluation['hit_rate']:.2%}")
    # print()

    for result in evaluation["results"]:
        status = (
            "PASS"
            if result["hit"]
            else "FAIL"
        )

        # print(
        #     f"[{status}] "
        #     f"{result['id']}: "
        #     f"{result['question']}"
        # )

        # print(
        #     f"  Expected: "
        #     f"{result['expected_sources']}"
        # )

        # print(
        #     f"  Retrieved: "
        #     f"{result['retrieved_sources']}"
        # )


if __name__ == "__main__":
    main()