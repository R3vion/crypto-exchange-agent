from pathlib import Path

from src.database import initialize_database
from src.exchanges import initialize_exchange_registry
from src.ingestion.esma import load_esma_casps, normalize_esma_casps, save_regulatory_status


ESMA_CSV = Path("data/raw/regulatory/esma/mica_casps.csv")

def main():
    print("Initializing database...")
    initialize_database()

    print("Initializing exchange registry...")
    initialize_exchange_registry()

    print(f"Loading ESMA data from: {ESMA_CSV}")
    dataframe = load_esma_casps(ESMA_CSV)
    print(f"Loaded {len(dataframe)} ESMA records.")

    normalized = normalize_esma_casps(dataframe)
    print(f"Normalized {len(normalized)} valid records.")

    inserted = save_regulatory_status(normalized, source="ESMA MiCA CASP Register")
    print(f"Successfully processed {inserted} records.")

if __name__ == "__main__":
    main()