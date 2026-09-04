from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

from src.database import get_connection


EXPECTED_COLUMNS = {
    "Name",
    "Commercial Name",
    "Types",
    "Country",
    "NCA",
    "Authorization Date",
    "LEI",
    "Website",
}


def load_esma_casps(csv_path: str | Path) -> pd.DataFrame:
    """Load and validate the ESMA CASP CSV."""

    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"ESMA CSV not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)

    missing_columns = EXPECTED_COLUMNS - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"ESMA CSV is missing columns: {sorted(missing_columns)}")

    return dataframe


def normalize_esma_casps(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Convert the ESMA schema into our internal schema."""

    normalized = dataframe.rename(
        columns={
            "Name": "legal_name",
            "Commercial Name": "commercial_name",
            "Country": "country",
            "NCA": "regulator",
            "Authorization Date": "authorization_date",
            "LEI": "lei",
            "Website": "website"
        }
    ).copy()

    normalized = normalized[["legal_name", "commercial_name", "country", "regulator", "authorization_date", "lei", "website"]]
    normalized = normalized.dropna(subset=["legal_name", "country"])
    for column in ["legal_name", "commercial_name", "country", "regulator", "authorization_date", "lei", "website"]:
        normalized[column] = normalized[column].fillna("").astype(str).str.strip()

    return normalized


def save_regulatory_status(dataframe: pd.DataFrame, source: str) -> int:
    """Store normalized regulatory records in SQLite."""

    retrieved_at = datetime.now(timezone.utc).isoformat()

    records = []
    for row in dataframe.itertuples(index=False):
        records.append(
            row.legal_name,
            row.commercial_name,
            row.country,
            row.regulator,
            row.authorization_date,
            row.lei or None,
            row.website,
            source,
            retrieved_at
        )

    with get_connection() as connection:
        connection.executemany(
            """
            INSERT INTO regulatory_status (
                legal_name,
                commercial_name,
                country,
                regulator,
                authorization_date,
                lei,
                website,
                source,
                source_retrieved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(lei) DO UPDATE SET
                legal_name = excluded.legal_name,
                commercial_name = excluded.commercial_name,
                country = excluded.country,
                regulator = excluded.regulator,
                authorization_date = excluded.authorization_date,
                website = excluded.website,
                source = excluded.source,
                source_retrieved_at = excluded.source_retrieved_at
            """,
            records,
        )

        connection.commit()

    return len(records)