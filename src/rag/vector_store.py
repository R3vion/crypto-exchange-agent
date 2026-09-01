from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.config import QDRANT_COLLECTION, QDRANT_URL


def create_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def initialize_collection(
    client: QdrantClient,
    vector_size: int,
) -> None:
    collections = client.get_collections().collections

    collection_names = {
        collection.name
        for collection in collections
    }

    if QDRANT_COLLECTION not in collection_names:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )