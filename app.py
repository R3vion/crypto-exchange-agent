import streamlit as st
import random
import time

from src.agent.graph import build_graph

EXAMPLE_QUESTIONS = [
    "What is MiCA?",
    "What is the purpose of MiCA?",
    "What is a CASP under MiCA?",
    "What MiCA authorization does Coinbase have in the EU?",
    "What MiCA authorization does Kraken have?",
    "What MiCA licenses does Bitpanda have?",
    "What are Coinbase Advanced trading fees?",
    "What are Kraken trading fees?",
    "What security measures does Bitpanda describe?",
    "Which exchange is the riskiest and why?",
    "Compare Coinbase, Kraken and Bitpanda under MiCA.",
    "Which exchange has the strongest regulatory position in the EU?",
    "Which exchange is the best long-term choice under MiCA?",
    "Which exchange has the lowest trading cost?",
    "Kraken or Coinbase is riskier and why?",
    "How much would I pay in fees for a $10,000 Coinbase trade?",
    "How much would I pay in fees for a $5,000 Kraken spot trade?",
    "where can I trade futures of the available exchanges?"
]


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

# Initialize example questions
if "example_questions" not in st.session_state:
    st.session_state["example_questions"] = random.sample(
        EXAMPLE_QUESTIONS,
        3,
    )


# Callback for example buttons
def select_example(question):
    st.session_state["question"] = question
    st.session_state["analyze_from_example"] = True


st.text_input(
    "Ask a question",
    placeholder=(
        "Ask about regulation, fees, security or risk... On 5 exchanges: CoinBase, Kraken, Bitpanda, Binance, CoinCash"
    ),
    key="question",
)

with st.container(horizontal=True):
    for example in st.session_state["example_questions"]:
        st.button(
            example,
            key=f"example_{example}",
            type="tertiary",
            on_click=select_example,
            args=(example,),
        )

if st.button("Show 3 new examples", type="tertiary"):
    st.session_state["example_questions"] = random.sample(EXAMPLE_QUESTIONS, 3)
    st.rerun()


st.write("\n")
st.write("\n")
st.write("\n")

analyze_clicked = st.button("Analyze")


if (st.session_state.get("analyze_from_example", False) or analyze_clicked):
    st.session_state["analyze_from_example"] = False

    question = st.session_state["question"]

    if not question:
        st.warning("Please enter a question first.")
    else:
        graph = get_graph()

        start_time = time.perf_counter()
        status = st.empty()

        with st.spinner("Analyzing..."):
            result = graph.invoke(
                {
                    "question": question,
                }
            )

        elapsed = time.perf_counter() - start_time
        status.write(f"Analysis completed in {elapsed:.1f} seconds")

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

        coverage_score = result.get("coverage_score")
        rag_iterations = result.get("rag_iterations")

        if coverage_score is not None or rag_iterations is not None:
            st.write("**RAG diagnostics**")
            col1, col2, col3 = st.columns([0.1, 0.1, 0.8])

            with col1:
                if coverage_score is not None:
                    st.metric(
                        "Coverage score",
                        f"{coverage_score:.2f}",
                    )

            with col2:
                if rag_iterations is not None:
                    st.metric(
                        "RAG iterations",
                        rag_iterations,
                    )

            with col3:
                if coverage_score is not None:
                    if coverage_score >= 0.75:
                        st.success("RAG evidence coverage is sufficient.")
                    else:
                        st.warning("RAG evidence coverage is below the target threshold.")

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