import json
import statistics
import numpy as np
import time
from pathlib import Path

from src.agent.graph import build_graph


class LoadTest:
    def __init__(self):
        self.QUESTIONS_PATH = Path("data/evaluation/questions.json")
        self.NUM_QUERIES = 150

        self.graph = build_graph()

        self.latencies = []
        self.rag_iterations = []
        self.test_iter = 0
    
    def main(self):
        questions = json.loads(self.QUESTIONS_PATH.read_text(encoding="utf-8"))

        queries = [item["question"] for item in questions]

        for index in range(self.NUM_QUERIES):
            question = queries[index % len(queries)]

            start = time.perf_counter()

            result = self.graph.invoke(
                {
                    "question": question,
                }
            )

            elapsed = time.perf_counter() - start

            print(f"{index + 1}/{self.NUM_QUERIES}: {elapsed:.2f}s")

            self.test_iter = index + 1
            self.latencies.append(elapsed)
            self.rag_iterations.append(result.get("rag_iterations", 0))


if __name__ == "__main__":
    instance = LoadTest()
    try:
        instance.main()
    except KeyboardInterrupt:
        print("\n\n=== Keyboard interrupt ===\n\n")
        print(f"{instance.test_iter} PCS query was executed")

    latencies = instance.latencies
    rag_iterations = instance.rag_iterations

    if len(latencies) > 0 and len(rag_iterations) > 0:
        print()
        print("Load test results")
        print("-----------------")
        print(f"Queries: {len(latencies)}")
        print(f"Mean: {np.mean(latencies):.2f}s")
        print(f"Median: {np.median(latencies):.2f}s")
        print(f"P95: {np.quantile(latencies, 0.95):.2f}s")
        print(f"P90: {np.quantile(latencies, 0.90):.2f}s")
        print(f"P85: {np.quantile(latencies, 0.85):.2f}s")
        print(f"P80: {np.quantile(latencies, 0.80):.2f}s")
        print(f"P75: {np.quantile(latencies, 0.75):.2f}s")
        print(f"P70: {np.quantile(latencies, 0.70):.2f}s")
        print(f"P65: {np.quantile(latencies, 0.65):.2f}s")
        print(f"P60: {np.quantile(latencies, 0.60):.2f}s")
        print(f"P55: {np.quantile(latencies, 0.55):.2f}s")
        print(f"P50: {np.quantile(latencies, 0.50):.2f}s")
        print(f"Min: {min(latencies):.2f}s")
        print(f"Max: {max(latencies):.2f}s")
        print(f"Avg RAG iter count: {np.mean(rag_iterations):.2f}")

    