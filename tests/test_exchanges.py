from src.database import initialize_database
from src.exchanges import (
    initialize_exchange_registry,
    resolve_exchange,
)


def setup_module():
    initialize_database()
    initialize_exchange_registry()


def test_resolve_coinbase():
    result = resolve_exchange("Coinbase")

    assert result is not None
    assert result["canonical_name"] == "Coinbase"


def test_resolve_case_insensitive():
    result = resolve_exchange("COINBASE")

    assert result is not None
    assert result["canonical_name"] == "Coinbase"


def test_resolve_unknown_exchange():
    result = resolve_exchange("Unknown Exchange")

    assert result is None