from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DocumentMetadata:
    source: str
    source_type: str
    exchange: str | None
    jurisdiction: str | None
    document_type: str
    url: str
    published_at: datetime | None = None


@dataclass(frozen=True)
class SourceDocument:
    content: str
    metadata: DocumentMetadata