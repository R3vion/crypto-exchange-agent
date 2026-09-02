import json
import statistics
import time
from pathlib import Path

from src.agent.graph import build_graph


QUESTIONS_PATH = Path(
    "data/evaluation/questions.json"
)

NUM_QUERIES = 75


def main():
    questions = json.loads(
        QUESTIONS_PATH.read_text(
            encoding="utf-8"
        )
    )

    queries = [
        item["question"]
        for item in questions
    ]

    graph = build_graph()

    latencies = []

    for index in range(NUM_QUERIES):
        question = queries[
            index % len(queries)
        ]

        start = time.perf_counter()

        graph.invoke(
            {
                "question": question,
            }
        )

        elapsed = (
            time.perf_counter() - start
        )

        latencies.append(elapsed)

        print(
            f"{index + 1}/{NUM_QUERIES}: "
            f"{elapsed:.2f}s"
        )

    print()
    print("Load test results")
    print("-----------------")
    print(
        f"Queries: {len(latencies)}"
    )
    print(
        f"Mean: {statistics.mean(latencies):.2f}s"
    )
    print(
        f"Median: {statistics.median(latencies):.2f}s"
    )
    print(
        f"P95: {statistics.quantiles(latencies, n=20)[18]:.2f}s"
    )
    print(
        f"Min: {min(latencies):.2f}s"
    )
    print(
        f"Max: {max(latencies):.2f}s"
    )


if __name__ == "__main__":
    main()