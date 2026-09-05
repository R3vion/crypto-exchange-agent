# Agentic RAG Crypto Exchange Research Assistant

## 1. Problem

This project is an agentic RAG prototype for crypto-exchange research and comparison.

The assistant helps users compare exchanges such as Coinbase, Kraken, Bitpanda, Binance and CoinCash using publicly available regulatory, fee, security and legal information.

Example questions:

* Which exchange has the strongest MiCA position?
* Which exchange is the riskiest and why?
* What are the trading fees?
* How much would a specific trade cost?
* Which exchange is the best long-term choice under MiCA?

The system is designed as a research and decision-support assistant, not as personalized financial advice.

## 2. Why Agentic RAG?

A simple RAG pipeline would retrieve documents and generate an answer.

This project uses an agentic workflow because different questions require different actions.

For example:

* regulatory questions require retrieval;
* fee questions require retrieval and calculation;
* risk questions require retrieval and risk scoring;
* comparison questions require evidence from multiple exchanges.

The LLM is responsible for query understanding and evidence evaluation, while deterministic Python code performs calculations and risk scoring.

## 3. Architecture

```text
User
 │
 ▼
Query Analyzer
 │
 ▼
Conditional Router
 │
 ├── RAG Subgraph
 │      │
 │      ├── Retrieve
 │      ├── Coverage Evaluation
 │      └── Bounded Loop
 │           max 3 iterations
 │
 ├── Calculator
 │
 └── Risk Scoring
        │
        ▼
Evidence Review
        │
        ▼
Answer Generator
        │
        ▼
Guardrails
        │
        ▼
Final Answer
```

## 4. RAG Subgraph

The RAG component is implemented as a dedicated LangGraph subgraph.

It uses iterative retrieval:

```text
Retrieve
   ↓
Evaluate coverage
   ↓
coverage sufficient?
   ├── yes → END
   └── no
        ↓
   Retrieve again
```

The loop is bounded to a maximum of *three* iterations.

The LLM evaluates a coverage score between 0 and 1 and identifies missing information.

The Python router makes the final loop decision deterministically.

## 5. Tools

### Calculator

The Calculator performs deterministic fee calculations.

`Decimal` is used instead of relying directly on binary floating-point arithmetic.

### Risk Scoring

The Risk Scoring tool calculates a weighted prototype risk score using:

* regulatory risk: 30%
* security risk: 30%
* transparency risk: 20%
* operational risk: 20%

The score is a prototype analytical framework and is not an objective financial rating.

## 6. Guardrails

The final answer passes through a basic deterministic guardrail layer.

The system blocks outputs containing explicit investment guarantees or direct personalized investment instructions.

The assistant also instructs the answer generator not to invent facts or present uncertain information as certain.

## 7. Data

The prototype uses publicly available textual sources, including regulatory and exchange documentation.

Regulatory information includes ESMA MiCA material and the ESMA CASP register.

Exchange-specific material includes public regulatory, fee, legal and security documentation.

The documents are stored under:

```text
data/raw/
```

## 8. Technology

* Python
* LangGraph
* LangChain
* Qdrant
* Ollama
* Qwen 27B
* Streamlit
* Docker
* pytest


## 9. Evaluation

The project contains a 20-question evaluation set covering:

* MiCA and regulation
* exchange-specific information
* fees
* risk
* comparison across different exchanges
* fee calculation
* risk calculations

Run:

```bash
python -m scripts.run_evaluation
```

The evaluation measures routing accuracy against expected operations.

## 10. Load Test

A 75-query load test is provided.

Run:

```bash
python -m scripts.load_test
```

The script reports:

* mean latency
* median latency
* P95 latency
* minimum latency
* maximum latency

The main expected bottleneck is local LLM inference time, especially because query analysis, coverage evaluation and answer generation require model inference.

## 11. Performance Optimizations

### Bounded RAG iteration

The RAG loop is limited to 3 iterations to prevent runaway latency.

### Conditional execution

Only the required tools are executed for a given query.

For example, the Risk Scoring tool is not executed for a normal regulatory lookup.

## 12. Local Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Qdrant and Ollama locally.

Pull the configured model:

```bash
ollama pull qwen3.6:27B
```

Run the application:

```bash
streamlit run app.py
```

## 13. Testing

Run the full test suite:

```bash
pytest -v
```

The test suite covers:

* query analysis
* graph routing
* RAG retrieval
* RAG coverage loop
* calculator tool call
* fee extraction
* risk scoring tool call
* evidence review
* answer generation
* guardrails
* end-to-end graph execution

## 14. Limitations

This is a prototype software.

The risk score is a deterministic analytical framework, not a regulated or objective risk rating.

The knowledge base contains a limited set of public documents and therefore cannot represent every exchange, jurisdiction or market condition.

The model runs locally through Ollama, so latency depends strongly on available hardware.

## 15. Reproducibility

The project keeps source documents, evaluation questions, tests and configuration in the repository so that the core experiments can be reproduced locally.

No paid API is required.
