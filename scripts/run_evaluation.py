import json
from pathlib import Path

from src.agent.graph import build_graph

QUESTIONS_PATH = Path("data/evaluation/questions.json")


def main():
    questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))

    graph = build_graph()

    passed = 0
    for item in questions:
        result = graph.invoke(
            {
                "question": item["question"],
            }
        )

        actual = result["query_analysis"].operation
        expected = item["expected_operation"]

        success = actual == expected

        if success:
            passed += 1

        print(
            f'{item["id"]}: '
            f'expected={expected}, '
            f'actual={actual}, '
            f'passed={success}'
        )

    accuracy = passed / len(questions)

    print(f"\nRouting accuracy: {accuracy:.1%}")


if __name__ == "__main__":
    main()