from pathlib import Path
from pypdf import PdfReader

from src.rag.models import DocumentMetadata, SourceDocument

"""
Ha egy konkrét PDF rosszul parse-olható,
akkor kezeljük azt a problémát,
amikor ténylegesen találkozunk vele.
"""


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