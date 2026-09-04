from src.database import get_connection


EXCHANGES = {
    "bitpanda": {
        "canonical_name": "Bitpanda",
        "website": "https://www.bitpanda.com",
        "primary_jurisdiction": "EU",
        "aliases": [
            "bitpanda",
        ],
    },
    "coinbase": {
        "canonical_name": "Coinbase",
        "website": "https://www.coinbase.com",
        "primary_jurisdiction": "US",
        "aliases": [
            "coinbase",
            "coinbase exchange",
        ],
    },
    "binance": {
        "canonical_name": "Binance",
        "website": "https://www.binance.com",
        "primary_jurisdiction": "Global",
        "aliases": [
            "binance",
            "binance exchange",
        ],
    },
    "kraken": {
        "canonical_name": "Kraken",
        "website": "https://www.kraken.com",
        "primary_jurisdiction": "US",
        "aliases": [
            "kraken",
            "kraken exchange",
        ],
    },
    "coincash": {
        "canonical_name": "CoinCash",
        "website": "https://coincash.eu",
        "primary_jurisdiction": "EU",
        "aliases": [
            "coincash",
            "coin cash",
        ],
    },
}


def initialize_exchange_registry():
    with get_connection() as connection:
        for exchange in EXCHANGES.values():
            cursor = connection.execute(
                """
                INSERT INTO exchanges (
                    canonical_name,
                    website,
                    primary_jurisdiction
                )
                VALUES (?, ?, ?)
                ON CONFLICT(canonical_name)
                DO UPDATE SET
                    website = excluded.website,
                    primary_jurisdiction =
                        excluded.primary_jurisdiction
                """,
                (
                    exchange["canonical_name"],
                    exchange["website"],
                    exchange["primary_jurisdiction"],
                ),
            )

            exchange_id = cursor.lastrowid

            if exchange_id == 0:
                exchange_id = connection.execute(
                    """
                    SELECT id
                    FROM exchanges
                    WHERE canonical_name = ?
                    """,
                    (exchange["canonical_name"],),
                ).fetchone()["id"]

            for alias in exchange["aliases"]:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO exchange_aliases (
                        exchange_id,
                        alias
                    )
                    VALUES (?, ?)
                    """,
                    (exchange_id, alias.lower()),
                )

        connection.commit()

def resolve_exchange(name: str) -> dict | None:
    normalized_name = name.strip().lower()

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                e.id,
                e.canonical_name,
                e.website,
                e.primary_jurisdiction
            FROM exchanges e
            JOIN exchange_aliases ea
                ON ea.exchange_id = e.id
            WHERE ea.alias = ?
            """,
            (normalized_name,),
        ).fetchone()

    return dict(row) if row else None