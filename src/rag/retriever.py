from src.config import QDRANT_COLLECTION, QDRANT_URL
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue
from src.rag.embeddings import create_embeddings


def retrieve(query:str, limit:int=5, exchange:str=None, jurisdiction:str=None, source_type:str=None) -> list[dict]:
    embeddings = create_embeddings()
    query_vector = embeddings.embed_query(query)

    client = QdrantClient(url=QDRANT_URL)

    conditions = []
    if exchange:
        conditions.append(FieldCondition(key="exchange", match=MatchValue(value=exchange)))

    if jurisdiction:
        conditions.append(FieldCondition(key="jurisdiction", match=MatchValue(value=jurisdiction)))

    if source_type:
        conditions.append(FieldCondition(key="source_type", match=MatchValue(value=source_type)))

    query_filter = None
    if conditions:
        query_filter = Filter(must=conditions)

    results = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector,
        query_filter=query_filter,
        limit=limit,
    )

    result = []
    for point in results.points:
        result.append(
            {
                "id": str(point.id),
                "text": point.payload["text"],
                "metadata": {key: value for key, value in point.payload.items() if key != "text"},
                "score": point.score,
            }
        )
    return result