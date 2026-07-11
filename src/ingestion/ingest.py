"""Pipeline de ingestao: extrai, faz chunking, gera embeddings e sobe para o Qdrant.

Uso:
    uv run python -m src.ingestion.ingest
"""

from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from src.config import settings
from src.embeddings.embedder import embed_texts
from src.ingestion.chunk import chunk_documents
from src.ingestion.extract import load_all_documents

EMBEDDING_DIM = 1536  # dimensao do text-embedding-3-small


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)


def ensure_collection(client: QdrantClient) -> None:
    if not client.collection_exists(settings.qdrant_collection):
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


def run(batch_size: int = 64) -> None:
    docs = load_all_documents()
    print(f"{len(docs)} documentos carregados de data/raw")

    chunks = chunk_documents(docs)
    print(f"{len(chunks)} chunks gerados")

    client = get_qdrant_client()
    ensure_collection(client)

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        vectors = embed_texts([c["text"] for c in batch])
        points = [
            PointStruct(
                id=i + idx,
                vector=vector,
                payload={"text": c["text"], **c["metadata"]},
            )
            for idx, (c, vector) in enumerate(zip(batch, vectors))
        ]
        client.upsert(collection_name=settings.qdrant_collection, points=points)
        print(f"Upsert de {len(points)} pontos ({i + len(points)}/{len(chunks)})")

    print("Ingestao concluida.")


if __name__ == "__main__":
    run()
