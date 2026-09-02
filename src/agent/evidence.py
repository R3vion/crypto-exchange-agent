from pydantic import BaseModel, Field

from src.agent.graph_state import AgentState
from src.llm import create_llm


class EvidenceReview(BaseModel):
    evidence_sufficient: bool = Field(
        description="Whether the available evidence is sufficient to answer the question reliably."
    )

    summary: str = Field(
        description="Short summary of the evidence that can be used in the final answer."
    )


def evidence_review_node(state: AgentState) -> AgentState:
    llm = create_llm().with_structured_output(
        EvidenceReview
    )

    question = state["question"]

    documents = state.get(
        "retrieved_documents",
        [],
    )

    tool_results = state.get(
        "tool_results",
        [],
    )

    document_text = "\n\n".join(
        [
            f"Document {index + 1}:\n{doc.get('text', '')}"
            for index, doc in enumerate(documents)
        ]
    )

    tool_text = "\n\n".join(
        [
            f"Tool result {index + 1}:\n{tool}"
            for index, tool in enumerate(tool_results)
        ]
    )

    prompt = f"""
You are the evidence review step of a financial
crypto-exchange research assistant.

User question:
{question}

Retrieved evidence:
{document_text}

Tool results:
{tool_text}

Review the available evidence.

Rules:
1. Use only the provided evidence and tool results.
2. Do not invent facts.
3. Decide whether the evidence is sufficient to answer
   the user's question.
4. Clearly identify the useful evidence.
5. If important evidence is missing, mark the evidence
   as insufficient.
6. Keep the summary concise.
"""

    review = llm.invoke(prompt)

    return {
        "evidence_summary": review.summary,
        "evidence_sufficient": review.evidence_sufficient,
    }