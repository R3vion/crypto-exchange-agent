from pathlib import Path
from pypdf import PdfReader
import yaml

from src.rag.models import DocumentMetadata, SourceDocument

def load_pdf(path, metadata: DocumentMetadata) -> SourceDocument:
    """Load text from a PDF document."""

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF document not found: {path}")

    reader = PdfReader(path)

    pages = []
    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text.strip().replace('\n\n', '\n'))

    content = "\n\n".join(pages).strip()

    if not content:
        raise ValueError(f"No extractable text found in PDF: {path}")

    return SourceDocument(content=content, metadata=metadata)


def load_manifest(manifest_path) -> list[tuple[str, DocumentMetadata]]:
    manifest_path = Path(manifest_path)

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with manifest_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    documents = []
    for item in data.get("documents", []):
        metadata = DocumentMetadata(
            source=item["source"],
            source_type=item["source_type"],
            exchange=item.get("exchange"),
            jurisdiction=item.get("jurisdiction"),
            document_type=item["document_type"],
            url=item["url"],
        )

        documents.append((item["file"], metadata))

    return documents