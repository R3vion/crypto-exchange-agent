from src.rag.retriever import retrieve

coinbase = retrieve(
    "Which exchange is riskier and why? Focus specifically on Coinbase.",
    exchange="Coinbase",
    limit=5,
)

kraken = retrieve(
    "Which exchange is riskier and why? Focus specifically on Kraken.",
    exchange="Kraken",
    limit=5,
)

print("\nCOINBASE")
for doc in coinbase:
    print(doc["metadata"].get("exchange"))
    print(doc["text"][:200])
    print()

print("\nKRAKEN")
for doc in kraken:
    print(doc["metadata"].get("exchange"))
    print(doc["text"][:200])
    print()