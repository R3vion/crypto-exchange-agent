import sqlite3
from pathlib import Path

from src.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection and ensure the database directory exists."""
    database_path = Path(DATABASE_PATH)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create the database schema if it does not exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS regulatory_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                legal_name TEXT NOT NULL,
                commercial_name TEXT,
                country TEXT NOT NULL,
                regulator TEXT,
                authorization_date TEXT,
                lei TEXT UNIQUE,
                website TEXT,
                source TEXT NOT NULL,
                source_retrieved_at TEXT NOT NULL
            )
            """
        )

        

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS exchanges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                canonical_name TEXT NOT NULL UNIQUE,
                website TEXT,
                primary_jurisdiction TEXT
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS exchange_aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exchange_id INTEGER NOT NULL,
                alias TEXT NOT NULL UNIQUE,
                FOREIGN KEY (exchange_id) REFERENCES exchanges(id)
            )
            """
        )

        connection.commit()