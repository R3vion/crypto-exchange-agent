import re


def extract_fee_rate(text:str) -> float | None:
    """
    Extract a simple percentage fee from retrieved text.

    Returns the fee as a decimal.
    Example:
        'Trading fee: 0.6%' -> 0.006
    """

    patterns = [
        r"(\d+(?:\.\d+)?)\s*%",
        r"(\d+(?:\.\d+)?)\s*percent",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if match:
            percentage = float(match.group(1))
            return percentage / 100

    return None