from src.rag.retriever import retrieve
from src.rag.state import RAGState
from src.llm import create_llm

from pydantic import BaseModel, Field

MAX_ITERATIONS = 3
COVERAGE_THRESHOLD = 0.75

class CoverageEvaluation(BaseModel):
    coverage_score: float = Field(
        ge=0.0,
        le=1.0,
        description="How well the retrieved documents cover the important information needed to answer the question.",
    )

    missing_information: list[str] = Field(
        default_factory=list,
        description="Important information that is still missing from the retrieved documents.",
    )

    improved_query: str = Field(
        description="A better retrieval query that targets the missing information.",
    )


def retrieve_documents(state: RAGState) -> RAGState:
    iteration = state.get("iteration", 0) + 1

    question = state["question"]
    retrieval_query = state.get("retrieval_query", question)

    exchanges = state.get("exchanges", [])
    exchange = exchanges[0] if len(exchanges) == 1 else None

    documents = retrieve(
        retrieval_query,
        limit=5,
        exchange=exchange,
    )

    existing_documents = state.get("retrieved_documents", [])

    # Avoid exact duplicates when we retrieve again.
    existing_ids = {
        doc.get("id")
        for doc in existing_documents
        if doc.get("id") is not None
    }

    merged_documents = list(existing_documents)

    for document in documents:
        document_id = document.get("id")

        if document_id is None or document_id not in existing_ids:
            merged_documents.append(document)

            if document_id is not None:
                existing_ids.add(document_id)

    return {
        "retrieved_documents": merged_documents,
        "iteration": iteration,
    }

def evaluate_coverage(state: RAGState) -> RAGState:
    llm = create_llm().with_structured_output(CoverageEvaluation)

    question = state["question"]
    documents = state.get("retrieved_documents", [])

    document_text = "\n\n".join(
        [
            f"Document {index + 1}:\n{doc.get('text', '')}"
            for index, doc in enumerate(documents)
        ]
    )

    prompt = f"""
You are evaluating retrieval quality for a RAG system.

User question:
{question}

Retrieved documents:
{document_text}

Evaluate how well the retrieved documents cover the information
required to answer the user's question.

Rules:

1. coverage_score must be between 0 and 1.
2. 1.0 means the retrieved documents contain enough relevant evidence to answer the question reliably.
3. 0.0 means the documents contain almost no useful evidence.
4. Consider all important aspects of the question.
5. Do not judge whether the answer itself is correct.
6. Identify important missing information.
7. If information is missing, create an improved retrieval query.
8. Do not invent facts.
"""

    evaluation = llm.invoke(prompt)

    return {
        "coverage_score": evaluation.coverage_score,
        "coverage_sufficient": evaluation.coverage_score,
        "retrieval_query": evaluation.improved_query,
    }


def route_after_coverage(state: RAGState) -> str:
    coverage_score = state.get("coverage_score", 0.0)
    iteration = state.get("iteration", 0)

    if coverage_score >= COVERAGE_THRESHOLD:
        return "complete"

    if iteration >= MAX_ITERATIONS:
        return "complete"

    return "retrieve_again"