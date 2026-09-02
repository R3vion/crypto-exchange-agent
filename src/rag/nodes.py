from pydantic import BaseModel, Field

from src.llm import create_llm
from src.rag.retriever import retrieve
from src.rag.state import RAGState


MAX_ITERATIONS = 3
COVERAGE_THRESHOLD = 0.65
TOP_K = 5


class CoverageEvaluation(BaseModel):
    coverage_score: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Overall retrieval coverage. "
            "1.0 means sufficient evidence, "
            "0.0 means almost no useful evidence."
        ),
    )

    coverage_by_exchange: dict[str, float] = Field(
        default_factory=dict,
        description=(
            "Coverage score for each requested exchange. "
            "Keys must be exchange names."
        ),
    )

    missing_information: list[str] = Field(
        default_factory=list,
        description="Important information still missing.",
    )

    improved_query: str = Field(
        description=(
            "A better retrieval query targeting the missing information."
        ),
    )


def retrieve_documents(state: RAGState) -> RAGState:
    print("\n=== RAG RETRIEVAL DEBUG ===")
    print("iteration:", state.get("iteration", 0) + 1)
    print("question:", state["question"])
    print("exchanges:", state.get("exchanges", []))
    print("retrieval_query:", state.get("retrieval_query"))
    print("===========================\n")

    iteration = state.get("iteration", 0) + 1

    question = state["question"]
    retrieval_query = state.get("retrieval_query", question)

    exchanges = state.get("exchanges", [])

    existing_documents = state.get(
        "retrieved_documents",
        [],
    )

    existing_ids = {
        doc.get("id")
        for doc in existing_documents
        if doc.get("id") is not None
    }

    merged_documents = list(existing_documents)

    if exchanges:
        # Entity-aware retrieval.
        #
        # For comparison questions we retrieve separately
        # for every requested exchange.
        for exchange in exchanges:
            entity_query = (
                f"{retrieval_query}\n"
                f"Focus specifically on {exchange}."
            )

            print(f"Retrieving for exchange: {exchange}")
            print(f"Query: {entity_query}")

            documents = retrieve(
                entity_query,
                limit=TOP_K,
                exchange=exchange,
            )

            print(
                "Retrieved:",
                [
                    doc["metadata"].get("exchange")
                    for doc in documents
                ],
            )

            for document in documents:
                document_id = document.get("id")

                if (
                    document_id is None
                    or document_id not in existing_ids
                ):
                    merged_documents.append(document)

                    if document_id is not None:
                        existing_ids.add(document_id)

    else:
        # Generic retrieval when no specific exchange was detected.
        documents = retrieve(
            retrieval_query,
            limit=TOP_K,
        )

        for document in documents:
            document_id = document.get("id")

            if (
                document_id is None
                or document_id not in existing_ids
            ):
                merged_documents.append(document)

                if document_id is not None:
                    existing_ids.add(document_id)

    return {
        "retrieved_documents": merged_documents,
        "iteration": iteration,
    }


def evaluate_coverage(state: RAGState) -> RAGState:
    llm = create_llm().with_structured_output(
        CoverageEvaluation
    )

    question = state["question"]
    exchanges = state.get("exchanges", [])
    documents = state.get("retrieved_documents", [])

    document_text = "\n\n".join(
        [
            (
                f"Document {index + 1}:\n"
                f"Exchange: "
                f"{doc.get('metadata', {}).get('exchange', 'unknown')}\n"
                f"{doc.get('text', '')}"
            )
            for index, doc in enumerate(documents)
        ]
    )

    exchange_instruction = ""

    if exchanges:
        exchange_instruction = f"""
The user explicitly mentioned these exchanges:

{exchanges}

For comparison questions, every requested exchange must
have relevant evidence.

Do not consider the retrieval complete if one requested
exchange has strong evidence but another has little or none.
"""

    prompt = f"""
You are evaluating retrieval quality for a RAG system.

User question:
{question}

Retrieved documents:
{document_text}

{exchange_instruction}

Evaluate whether the retrieved documents contain enough
relevant evidence to answer the question reliably.

Rules:

1. coverage_score must be between 0 and 1.

2. 1.0 means the retrieved documents contain enough
   relevant evidence to answer the question reliably.

3. 0.0 means the documents contain almost no useful evidence.

4. Consider all important aspects of the question.

5. Do not judge whether the final answer is correct.

6. Do not invent facts.

7. For comparison questions, evaluate each requested
   exchange separately.

8. If an exchange has insufficient evidence, its
   coverage score should be low.

9. If information is missing, create an improved retrieval
   query that specifically targets the missing information.

10. The improved query should be useful for another
    retrieval iteration.
"""

    evaluation = llm.invoke(prompt)

    coverage_by_exchange = evaluation.coverage_by_exchange

    missing_exchanges = [
        exchange
        for exchange in exchanges
        if coverage_by_exchange.get(exchange, 0.0)
        < COVERAGE_THRESHOLD
    ]

    if exchanges:
        coverage_sufficient = not missing_exchanges
    else:
        coverage_sufficient = (
            evaluation.coverage_score
            >= COVERAGE_THRESHOLD
        )

    return {
        "coverage_score": evaluation.coverage_score,
        "coverage_sufficient": coverage_sufficient,
        "coverage_by_exchange": coverage_by_exchange,
        "missing_exchanges": missing_exchanges,
        "retrieval_query": evaluation.improved_query,
    }


def route_after_coverage(state: RAGState) -> str:
    iteration = state.get("iteration", 0)
    coverage_sufficient = state.get(
        "coverage_sufficient",
        False,
    )

    if coverage_sufficient:
        return "complete"

    if iteration >= MAX_ITERATIONS:
        return "complete"

    return "retrieve_again"