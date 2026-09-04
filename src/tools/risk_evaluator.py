from pydantic import BaseModel, Field

from src.llm import create_llm


class RiskEvaluation(BaseModel):
    regulatory_risk: float = Field(ge=0, le=10)
    security_risk: float = Field(ge=0, le=10)
    transparency_risk: float = Field(ge=0, le=10)
    operational_risk: float = Field(ge=0, le=10)
    reasoning: list[str] = Field(default_factory=list)


def evaluate_risk_evidence(question :str, documents :list[dict]) -> RiskEvaluation:
    llm = create_llm().with_structured_output(RiskEvaluation)

    document_text = "\n\n".join(
        [
            f"Document {index + 1}:\n{doc.get('text', '')}"
            for index, doc in enumerate(documents)
        ]
    )

    prompt = f"""
You are evaluating risk evidence for a crypto exchange
decision-support system.

User question:
{question}

Evidence:
{document_text}

Evaluate ONLY the evidence provided.

Score each risk factor from 0 to 10:

0 = very low risk
10 = very high risk

Factors:

- regulatory_risk:
  Regulatory authorization, licensing, MiCA status,
  restrictions or regulatory concerns.

- security_risk:
  Evidence related to custody, security controls,
  security incidents or protection of assets.

- transparency_risk:
  Transparency of fees, legal information,
  policies and publicly available information.

- operational_risk:
  Evidence related to service availability,
  operational restrictions, geographic limitations
  or other operational concerns.

Important rules:

1. Do not invent facts.
2. Do not use outside knowledge.
3. Base the scores only on the retrieved evidence.
4. If evidence is missing, do not assume that the exchange
   is safe. Reflect uncertainty in the score.
5. Provide short reasoning for the scores.
"""

    return llm.invoke(prompt)