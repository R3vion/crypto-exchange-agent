import json
from pathlib import Path

from src.agent.graph import build_graph

QUESTIONS_PATH = Path("data/evaluation/questions.json")


def main():
    questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))

    graph = build_graph()

    passed = 0
    question_num = 0
    for i, item in enumerate(questions):
        try:
            expected = item["expected_operation"]
            question_num += 1
        except KeyError:
            continue

        result = graph.invoke(
            {
                "question": item["question"],
            }
        )

        actual = result["query_analysis"].operation

        success = actual == expected

        if success:
            passed += 1

        print(
            f'{item["id"]}: '
            f'expected={expected}, '
            f'actual={actual}, '
            f'passed={success}'
        )

    accuracy = passed / question_num

    print(f"\nRouting accuracy: {accuracy:.1%}")


if __name__ == "__main__":
    main()