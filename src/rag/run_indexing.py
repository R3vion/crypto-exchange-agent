from pathlib import Path

from src.rag.indexer import index_documents
from src.rag.loaders import load_pdf
from src.rag.manifest import load_manifest


DOCUMENT_ROOT = Path(
    "data/raw/documents"
)

MANIFEST_PATH = (
    DOCUMENT_ROOT / "manifest.yaml"
)


def main() -> None:
    manifest = load_manifest(
        MANIFEST_PATH
    )

    documents = []

    for relative_path, metadata in manifest:
        document_path = (
            DOCUMENT_ROOT / relative_path
        )

        print(
            f"Loading: {document_path}"
        )

        document = load_pdf(
            document_path,
            metadata,
        )

        documents.append(document)

    indexed = index_documents(
        documents
    )

    print(
        f"Successfully indexed {indexed} chunks."
    )


if __name__ == "__main__":
    main()