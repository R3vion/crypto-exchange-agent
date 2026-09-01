from src.tools.calculator import calculate_fee


def test_calculate_fee():
    result = calculate_fee(
        amount=1000,
        fee_rate=0.006,
    )

    assert result["fee"] == 6.0
    assert result["total"] == 1006.0


def test_calculate_zero_fee():
    result = calculate_fee(
        amount=1000,
        fee_rate=0,
    )

    assert result["fee"] == 0.0
    assert result["total"] == 1000.0