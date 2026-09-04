from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.models import SourceDocument


def chunk_document(document: SourceDocument) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=225,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    chunks = splitter.create_documents(
        texts=[document.content],
        metadatas=[
            {
                "source": document.metadata.source,
                "source_type": document.metadata.source_type,
                "exchange": document.metadata.exchange,
                "jurisdiction": document.metadata.jurisdiction,
                "document_type": document.metadata.document_type,
                "url": document.metadata.url,
                "published_at": (document.metadata.published_at.isoformat() if document.metadata.published_at else None)
            }
        ]
    )

    return chunks