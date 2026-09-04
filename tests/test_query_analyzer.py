from src.agent.query_analyzer import analyze_query


def test_query_analyzer():
    result = analyze_query("Which exchange is the best long-term choice under MiCA: Coinbase, Kraken or Bitpanda?")

    assert result.intent == "comparison"

    assert "Coinbase" in result.exchanges
    assert "Kraken" in result.exchanges
    assert "Bitpanda" in result.exchanges

    assert result.jurisdiction == "EU"

    assert result.requires_rag is True
    assert result.requires_risk_scoring is False


def test_query_analyzer_risk_question():
    result = analyze_query("Which exchange is the riskiest and why?")

    assert result.intent == "risk"

    assert result.requires_rag is True
    assert result.requires_risk_scoring is True