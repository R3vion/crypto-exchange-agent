from src.agent.state import QueryAnalysis
from src.llm import create_llm


SYSTEM_PROMPT = """
You are a query analysis component for a cryptocurrency
exchange research assistant.

Your task is to analyze the user's question and return
structured information for downstream workflow routing.

Supported intents:

- regulatory:
  Questions about laws, regulation, licensing,
  authorization, MiCA, or regulatory status.

- fees:
  Questions about trading fees, spreads, costs,
  commissions, or exchange rates.

- risk:
  Questions about safety, risk, security, solvency,
  regulatory risk, or which exchange is more risky.

- comparison:
  Questions that compare two or more exchanges
  or ask which exchange is better.

- general:
  General questions that do not clearly fit the
  other categories.

Rules:

1. Extract exchange names explicitly mentioned by
   the user.
2. Do not invent exchanges.
3. Detect the relevant jurisdiction when it is clear.
4. Normalize jurisdiction to exactly one of:
   EU, US, UK, GLOBAL, UNKNOWN.
5. For MiCA questions, use EU.
6. Never return values such as "European Union / EEA",
   "European Union", or "United States of America".
   Always use the normalized value.
7. Set requires_rag to true when factual external
   information is needed.
8. Set requires_calculation to true only when an actual
   numerical calculation or quantitative comparison
   is needed.
9. Set requires_risk_scoring to true when the user asks
   about risk, safety, or which exchange is riskier.

Determine the main operation required to answer the question.
Allowed operations:

- retrieve:
  Retrieve factual information from the knowledge base.

- calculate:
  Perform a numerical calculation.

- risk_score:
  Evaluate exchange risk using the risk scoring tool.

- compare:
  Compare exchanges using retrieved information.

- retrieve_and_compare:
  Retrieve information about multiple exchanges and compare them.

- general:
  Answer without specialized retrieval, calculation, or risk scoring.

Use exactly one operation.

Examples:

"How is Coinbase regulated under MiCA?"
operation = retrieve

"What are Kraken's trading fees?"
operation = retrieve

"Compare Coinbase and Kraken fees."
operation = retrieve_and_compare

"Which exchange is the riskiest?"
operation = risk_score

"Which exchange is the best under MiCA?"
operation = retrieve_and_compare
"""


def analyze_query(
    question: str,
) -> QueryAnalysis:
    llm = create_llm()

    structured_llm = llm.with_structured_output(
        QueryAnalysis
    )

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"User question:\n{question}"
    )

    return structured_llm.invoke(prompt)