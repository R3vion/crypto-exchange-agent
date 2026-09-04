from src.rag.evaluation import evaluate_retrieval, load_questions


def main():
    questions = load_questions("tests/data/retrieval_questions.yaml")
    evaluation = evaluate_retrieval(questions, top_k=5)

    print()
    print("Retrieval Evaluation")
    print("=====================")
    print(f"Questions: {evaluation['total']}")
    print(f"Hits:      {evaluation['hits']}")
    print(f"Hit rate:  {evaluation['hit_rate']:.2%}")
    print()

    for result in evaluation["results"]:
        if result["hit"]:
            status = "PASS"
        else:
            status = "FAIL"

        print(f"[{status}] {result['id']}: {result['question']}")
        print(f"\tExpected: {result['expected_sources']}")
        print(f"\tRetrieved: {result['retrieved_sources']}")


if __name__ == "__main__":
    main()