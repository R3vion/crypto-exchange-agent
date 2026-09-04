from src.tools.fee_extractor import extract_fee_rate


def test_extract_percentage_fee():
    text = "The trading fee is 0.6%."
    result = extract_fee_rate(text)
    assert result == 0.006


def test_extract_percent_fee():
    text = "The trading fee is 0.4 percent."
    result = extract_fee_rate(text)
    assert result == 0.004


def test_no_fee_found():
    text = "This document contains no fee information."
    result = extract_fee_rate(text)
    assert result is None