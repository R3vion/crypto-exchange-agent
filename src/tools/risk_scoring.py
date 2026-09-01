from dataclasses import dataclass


@dataclass
class RiskFactors:
    regulatory_risk: float
    security_risk: float
    transparency_risk: float
    operational_risk: float


def calculate_risk_score(factors: RiskFactors) -> dict:
    """
    Calculate a weighted exchange risk score.

    Each factor is between 0 and 10.
    Higher score means higher risk.
    """

    weights = {
        "regulatory_risk": 0.30,
        "security_risk": 0.30,
        "transparency_risk": 0.20,
        "operational_risk": 0.20,
    }

    values = {
        "regulatory_risk": factors.regulatory_risk,
        "security_risk": factors.security_risk,
        "transparency_risk": factors.transparency_risk,
        "operational_risk": factors.operational_risk,
    }

    for name, value in values.items():
        if not 0 <= value <= 10:
            raise ValueError(
                f"{name} must be between 0 and 10."
            )

    score = sum(
        values[name] * weights[name]
        for name in values
    )

    if score < 3.0:
        level = "low"
    elif score < 6.0:
        level = "medium"
    else:
        level = "high"

    return {
        "risk_score": round(score, 2),
        "risk_level": level,
        "factors": values,
        "weights": weights,
    }