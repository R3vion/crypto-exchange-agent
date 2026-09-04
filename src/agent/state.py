from typing import Literal

from pydantic import BaseModel, Field


Intent = Literal[
    "regulatory",
    "fees",
    "risk",
    "comparison",
    "general",
]


Operation = Literal[
    "retrieve",
    "calculate",
    "risk_score",
    "compare",
    "retrieve_and_compare",
    "general",
]


Jurisdiction = Literal[
    "EU",
    "US",
    "UK",
    "GLOBAL",
    "UNKNOWN",
]


class QueryAnalysis(BaseModel):
    intent: Intent = Field(
        description="The main intent of the user's question."
    )

    operation: Operation = Field(
        description="The main operation required to answer the user's question."
    )

    exchanges: list[str] = Field(
        default_factory=list,
        description="Cryptocurrency exchanges explicitly mentioned or clearly requested by the user."
    )

    jurisdiction: Jurisdiction = Field(
        default="UNKNOWN",
        description="Relevant jurisdiction. Use exactly one of: EU, US, UK, GLOBAL, UNKNOWN."
    )

    requires_rag: bool = Field(
        description="Whether external documents or structured knowledge are required."
    )

    requires_calculation: bool = Field(
        description="Whether numerical calculation or quantitative comparison is required."
    )

    requires_risk_scoring: bool = Field(
        description="Whether the risk scoring tool should be used."
    )

    calculation_amount: float | None = Field(
        default=None,
        description="Trade amount to use for a calculation, if provided."
    )

    fee_rate: float | None = Field(
        default=None,
        description="Fee rate as a decimal, if provided.",
    )

class ExchangeExtraction(BaseModel):
    exchanges: list[str] = Field(
        description="Exchanges from the provided supported exchange list that are relevant to the user's question."
    )