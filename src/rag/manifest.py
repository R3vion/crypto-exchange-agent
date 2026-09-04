from pathlib import Path
import yaml

from src.rag.models import DocumentMetadata


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