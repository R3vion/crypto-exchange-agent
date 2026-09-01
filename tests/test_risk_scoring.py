import pytest

from src.tools.risk_scoring import (
    RiskFactors,
    calculate_risk_score,
)


def test_risk_score():
    factors = RiskFactors(
        regulatory_risk=2,
        security_risk=4,
        transparency_risk=3,
        operational_risk=5,
    )

    result = calculate_risk_score(factors)

    assert result["risk_score"] == 3.4
    assert result["risk_level"] == "medium"


def test_high_risk():
    factors = RiskFactors(
        regulatory_risk=9,
        security_risk=9,
        transparency_risk=8,
        operational_risk=8,
    )

    result = calculate_risk_score(factors)

    assert result["risk_level"] == "high"


def test_invalid_risk_factor():
    factors = RiskFactors(
        regulatory_risk=11,
        security_risk=5,
        transparency_risk=5,
        operational_risk=5,
    )

    with pytest.raises(ValueError):
        calculate_risk_score(factors)