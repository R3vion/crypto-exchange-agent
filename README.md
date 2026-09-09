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

The agent is implemented as a LangGraph workflow. The `query_analyzer` determines the query type, while the graph routes non-general queries through the RAG pipeline before performing any required calculation or risk scoring.

```text
User
 │
 ▼
Query Analyzer
 │
 ├── general ──────────────────────────────┐
 │                                         │
 └── retrieve / compare / calculate /      │
     risk_score                            │
              │                            │
              ▼                            │
             RAG                           │
              │                            │
       ┌──────┼──────────┐                 │
       │      │          │                 │
       ▼      ▼          ▼                 │
 Calculator  Risk      Evidence Review     │
     Tool    Tool        │                 │
       │      │          │                 │
       └──────┴──────────┘                 │
              │                            │
              ▼                            │
       Answer Generator ◄──────────────────┘
              │
              ▼
          Guardrails
              │
              ▼
             END
```

For non-general queries, RAG is always executed first. After retrieval, the graph either performs a calculation, performs risk scoring, or continues directly to evidence review.

General queries bypass RAG and proceed directly to answer generation.


## 4. RAG Subgraph

The RAG component is implemented as a dedicated LangGraph subgraph with iterative retrieval.

```text
START
  │
  ▼
Retrieve Documents
  │
  ▼
Evaluate Coverage
  │
  ▼
Coverage sufficient?
  ├── Yes → END
  │
  └── No
       │
       ▼
  Retrieve Documents
       │
       └── repeat
```

After each retrieval, the LLM evaluates the evidence coverage and identifies missing information. A Python router uses this evaluation to decide whether another retrieval is required or the RAG process is complete.

The retrieval loop is bounded to a maximum of three iterations.


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

Routing accuracy: 95.0%, which means 19/20 PASSED.
The one which not passed can be seen below:
```
q18: expected=retrieve_and_compare, actual=risk_score, passed=False
=== QUERY ANALYZER DEBUG ===
question: What is Binance's current MiCA situation in the EU?
operation: retrieve
exchanges: ['Binance']
jurisdiction: EU
requires_risk_scoring: False
```

## 10. Load Test

A 150-query load test is provided.

Run:

```bash
python -m scripts.load_test
```

### Load test results
|   Metrics   |  Value  |
| ----------- | ------- |
| Queries     |    150  |
| Mean        |  47.12s |
| Median      |  28.81s |
| P95 latency | 133.51s |
| Min         |  5.45s  |
| Max         | 158.43s |
| Avg RAG iter|   2.53  |

### Bottleneck Analysis

The main bottleneck is **local LLM inference**, as query analysis, RAG coverage evaluation, and answer generation each require model inference.

A second bottleneck is the **RAG retrieval loop**. The average was **2.53 iterations per query**, close to the maximum of 3. The small dataset often does not contain enough relevant evidence to reach the coverage threshold, causing additional retrieval attempts before the loop is terminated.

### Optimization

* Reduce the number of LLM calls by combining query analysis or coverage evaluation where possible.
* Improve document coverage and retrieval quality to reduce unnecessary RAG iterations.


## 11. Performance Optimizations

### Bounded RAG iteration

The RAG loop is limited to 3 iterations to prevent runaway latency.

### Conditional execution

Only the required tools are executed for a given query.

For example, the Risk Scoring tool is not executed for a normal regulatory lookup.

## 12. Environment Variables

* `OLLAMA_BASE_URL` — Base URL of the Ollama API used for LLM inference.
* `OLLAMA_MODEL` — Ollama model used for text generation and LLM inference.
* `EMBEDDING_MODEL` — Model used to generate vector embeddings for semantic search.
* `QDRANT_URL` — HTTP endpoint of the Qdrant vector database.
* `QDRANT_COLLECTION` — Qdrant collection used to store and retrieve document embeddings.
* `DATABASE_PATH` — Filesystem path to the SQLite database containing structured financial data.

for my application the **Qwen3.6:27B** Local LLM was chosen by default because its Q4_K_M quantization fits within the **24 GB VRAM of an RTX 3090**, allowing fully local inference without paid APIs. It also supports multiple languages and provides a **256K context window**.

The main trade-off is lower inference speed on consumer hardware. Local inference also lacks real-time knowledge, which is addressed in this project through **RAG**.

To run the application locally without docker with default values copy the `.env.example` file as `.env`


## 13. Local Setup

Optional: Activate Virtual Environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies (needed only for running load_test.py & run_evaluation.py):

```bash
pip install -r requirements.txt
```

<!-- Start Qdrant and Ollama locally. -->


Install Ollama to your computer from its Official site:
`https://ollama.com/`

Pull the configured models:

```bash
ollama pull qwen3.6:27B
ollama pull nomic-embed-text
```

### Start the Application via `docker-compose`

Run the application:

```bash
docker-compose up --build
```
The Streamlit App UI can be reached at http://localhost:80

## 14. Testing

Run the full test suite:

```bash
pytest -v
```

```
collected 31 items

test_graph_routes_comparison            PASSED [  3%]
test_graph_routes_risk                  PASSED [  6%]
test_comparison_routes_to_rag           PASSED [  9%]
test_risk_question_is_analyzed          PASSED [ 12%]
test_fee_calculation_routes_through_rag PASSED [ 16%]
test_risk_question_runs_risk_tool       PASSED [ 19%]
test_end_to_end_rag_question            PASSED [ 22%]
test_end_to_end_guardrails              PASSED [ 25%]
test_answer_generator                   PASSED [ 29%]
test_calculate_fee                      PASSED [ 32%]
test_calculate_zero_fee                 PASSED [ 35%]
test_esma_csv_exists                    PASSED [ 38%]
test_esma_csv_schema                    PASSED [ 41%]
test_esma_normalization                 PASSED [ 45%]
test_evidence_review                    PASSED [ 48%]
test_resolve_coinbase                   PASSED [ 51%]
test_resolve_case_insensitive           PASSED [ 54%]
test_resolve_unknown_exchange           PASSED [ 58%]
test_extract_percentage_fee             PASSED [ 61%]
test_extract_percent_fee                PASSED [ 64%]
test_no_fee_found                       PASSED [ 67%]
test_guardrails_allow_normal_answer     PASSED [ 70%]
test_guardrails_block_financial_advice  PASSED [ 74%]
test_llm_connection                     PASSED [ 77%]
test_query_analyzer                     PASSED [ 80%]
test_query_analyzer_risk_question       PASSED [ 83%]
test_rag_graph_returns_documents        PASSED [ 87%]
test_retrieval_returns_results          PASSED [ 90%]
test_risk_score                         PASSED [ 93%]
test_high_risk                          PASSED [ 96%]
test_invalid_risk_factor                PASSED [100%]

========== 31 passed in 719.73s (0:11:59) ==========
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

## 15. How to Create or Extend the Vector Database

The Docker Compose setup includes a pre-indexed vector database, so you **do not need to create a dataset to run the demo**.

If you want to **create a new dataset or add documents to the existing vector database**, follow these steps:

1. Place the PDF documents in `data/raw/documents/`.
2. Create `data/raw/documents/manifest.yaml` and add an entry for each PDF with its metadata.
3. Run the indexing script:

```bash
python -m scripts.run_indexing
```

Example `manifest.yaml`:

```yaml
documents:
  - file: regulatory/mica_document.pdf
    source: ESMA
    source_type: regulator
    exchange: null
    jurisdiction: EU
    document_type: regulation
    url: https://www.esma.europa.eu/
```

The `file` path is relative to `data/raw/documents/`.

The Qdrant dashboard is available at:
`http://localhost:6333/dashboard`


## 16. Limitations


This is a prototype software.

The risk score is a deterministic analytical framework, not a regulated or objective risk rating.

The knowledge base contains a limited set of public documents and therefore cannot represent every exchange, jurisdiction or market condition.

The model runs locally through Ollama, so latency depends strongly on available hardware.

## 17. Reproducibility

The project keeps source documents, evaluation questions, tests and configuration in the repository so that the core experiments can be reproduced locally.

No paid API is required.
