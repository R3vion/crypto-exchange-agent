from pathlib import Path

import yaml

from src.rag.retriever import retrieve


def load_questions(
    path: str | Path,
) -> list[dict]:
    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = yaml.safe_load(file)

    return data["questions"]


def evaluate_retrieval(
    questions: list[dict],
    top_k: int = 5,
) -> dict:
    hits = 0
    results = []

    for item in questions:
        retrieved = retrieve(
            item["question"],
            limit=top_k,
            exchange=(
                item["expected_exchanges"][0]
                if item["expected_exchanges"]
                else None
            ),
        )

        retrieved_sources = {
            result["metadata"]["source"]
            for result in retrieved
        }

        expected_sources = set(
            item["expected_sources"]
        )

        hit = bool(
            retrieved_sources
            & expected_sources
        )

        if hit:
            hits += 1

        results.append(
            {
                "id": item["id"],
                "question": item["question"],
                "hit": hit,
                "expected_sources": list(
                    expected_sources
                ),
                "retrieved_sources": list(
                    retrieved_sources
                ),
            }
        )

    total = len(questions)

    return {
        "total": total,
        "hits": hits,
        "hit_rate": (
            hits / total
            if total
            else 0.0
        ),
        "results": results,
    }