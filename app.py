import streamlit as st

from src.agent.graph import build_graph


st.set_page_config(
    page_title="Crypto Exchange Research Assistant",
    page_icon="₿",
    layout="wide",
)


@st.cache_resource
def get_graph():
    return build_graph()


st.title("Crypto Exchange Research Assistant")

st.write(
    "Agentic RAG assistant for comparing crypto exchanges "
    "using regulatory, fee, security and operational evidence."
)

question = st.text_input(
    "Ask a question",
    placeholder=(
        "Which exchange is the best long-term choice "
        "under MiCA?"
    ),
)

if st.button("Analyze") and question:
    graph = get_graph()

    with st.spinner("Analyzing..."):
        result = graph.invoke(
            {
                "question": question,
            }
        )

    # for key, value in result.items():
    #     print(f"\n\n\n{key}:\n{value}")

    st.subheader("Answer")

    st.write(
        result.get(
            "final_answer",
            "No answer was generated.",
        )
    )

    st.divider()

    st.subheader("Agent steps")

    analysis = result.get("query_analysis")

    if analysis:
        st.write("**Query Analysis**")

        st.json(
            {
                "intent": analysis.intent,
                "operation": analysis.operation,
                "exchanges": analysis.exchanges,
                "jurisdiction": analysis.jurisdiction,
                "requires_rag": analysis.requires_rag,
                "requires_calculation": (
                    analysis.requires_calculation
                ),
                "requires_risk_scoring": (
                    analysis.requires_risk_scoring
                ),
            }
        )

    documents = result.get(
        "retrieved_documents",
        [],
    )

    st.write(
        f"**Retrieved evidence:** {len(documents)} documents"
    )

    coverage_score = result.get("coverage_score")

    if coverage_score is not None:
        st.write(
            f"**RAG coverage score:** {coverage_score:.2f}"
        )

    tool_results = result.get(
        "tool_results",
        [],
    )

    if tool_results:
        st.write("**Tools used**")

        for tool_result in tool_results:
            st.json(tool_result)

    evidence_summary = result.get(
        "evidence_summary"
    )

    if evidence_summary:
        st.write("**Evidence review**")
        st.write(evidence_summary)

    st.write("**Retrieved documents**")

    for index, document in enumerate(documents, start=1):
        with st.expander(f"Document {index}"):
            st.write(document.get("text", ""))

            metadata = document.get(
                "metadata",
                {},
            )

            if metadata:
                st.json(metadata)