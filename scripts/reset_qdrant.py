from qdrant_client import QdrantClient

from src.config import QDRANT_COLLECTION, QDRANT_URL


def main():
    client = QdrantClient(url=QDRANT_URL)

    print(f"Deleting collection: {QDRANT_COLLECTION}")

    if client.collection_exists(QDRANT_COLLECTION):
        client.delete_collection(
            collection_name=QDRANT_COLLECTION
        )
        print("Collection deleted.")
    else:
        print("Collection does not exist.")

    print("Done.")


if __name__ == "__main__":
    main()