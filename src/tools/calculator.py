from decimal import Decimal # floating-point problem: 0.1 + 0.2 != 0.3


def calculate_fee(amount: float, fee_rate: float) -> dict:
    """
    Calculate trading fee and total cost.

    amount: trade amount in quote currency
    fee_rate: fee rate as decimal, e.g. 0.006 for 0.6%
    """

    amount_decimal = Decimal(str(amount))
    fee_rate_decimal = Decimal(str(fee_rate))

    fee = amount_decimal * fee_rate_decimal
    total = amount_decimal + fee

    return {
        "amount": float(amount_decimal),
        "fee_rate": float(fee_rate_decimal),
        "fee": float(fee),
        "total": float(total),
    }