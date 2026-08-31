from pathlib import Path

from src.ingestion.esma import (
    load_esma_casps,
    normalize_esma_casps,
)


CSV_PATH = Path(
    "data/raw/regulatory/esma/mica_casps.csv"
)


def test_esma_csv_exists():
    assert CSV_PATH.exists()


def test_esma_csv_schema():
    dataframe = load_esma_casps(CSV_PATH)

    expected_columns = {
        "Name",
        "Commercial Name",
        "Types",
        "Country",
        "NCA",
        "Authorization Date",
        "LEI",
        "Website",
    }

    assert expected_columns.issubset(
        dataframe.columns
    )


def test_esma_normalization():
    dataframe = load_esma_casps(CSV_PATH)
    normalized = normalize_esma_casps(dataframe)

    assert len(normalized) > 0

    assert "legal_name" in normalized.columns
    assert "country" in normalized.columns
    assert "regulator" in normalized.columns