import hashlib
import uuid

from src.config import QDRANT_COLLECTION
from qdrant_client.models import PointStruct
from src.rag.chunking import chunk_document
from src.rag.embeddings import create_embeddings
from src.rag.models import SourceDocument
from src.rag.vector_store import create_qdrant_client, initialize_collection


def create_chunk_id(source: str, url: str, text: str) -> str:
    value = f"{source}|{url}|{text}"
    digest = hashlib.sha256(value.encode("utf-8")).digest()

    return str(uuid.UUID(bytes=digest[:16]))


def index_documents(documents: list[SourceDocument]) -> int:
    embeddings = create_embeddings()
    client = create_qdrant_client()

    all_chunks = []
    for document in documents:
        all_chunks.append(chunk_document(document))

    if not all_chunks:
        return 0

    chunks = []
    for chunk in all_chunks:
        chunks.append(chunk.page_content)

    vectors = embeddings.embed_documents(chunks)
    initialize_collection(client, vector_size=len(vectors[0]))

    points = []
    for chunk, vector in zip(all_chunks, vectors, strict=True):
        chunk_id = create_chunk_id(
            chunk.metadata["source"],
            chunk.metadata["url"],
            chunk.page_content
        )

        points.append(PointStruct(
                id=chunk_id,
                vector=vector,
                payload={"text": chunk.page_content, **chunk.metadata}
            )
        )

    client.upsert(collection_name=QDRANT_COLLECTION, points=points)

    return len(points)