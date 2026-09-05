from src.agent.graph_state import AgentState
from src.llm import create_llm


def answer_generator_node(state: AgentState) -> AgentState:

    llm = create_llm()

    question = state["question"]
    evidence_summary = state.get("evidence_summary", "")
    tool_results = state.get("tool_results", [])
    evidence_sufficient = state.get("evidence_sufficient", False)

    prompt = f"""
You are a crypto-exchange research assistant.

User question:
{question}

Evidence summary:
{evidence_summary}

Tool results:
{tool_results}

Write a concise, evidence-based answer.

Rules:

1. Answer the user's actual question.
2. Use only the provided evidence.
3. Do not invent facts.
4. Do not present uncertain information as certain.
5. If comparing exchanges, explain the main reasons.
6. If a calculation result is available, show the result clearly.
7. Do not give personalized financial advice.
"""

    response = llm.invoke(prompt)

    if not evidence_sufficient:
        return {"final_answer": f"*I do not have enough reliable evidence to answer this question confidently.*\n\n{response.content}"}
    else:
        return {"final_answer": response.content}