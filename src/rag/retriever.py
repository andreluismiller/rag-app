"""Busca por similaridade no Qdrant."""

from __future__ import annotations

from qdrant_client import QdrantClient

from src.config import settings
from src.embeddings.embedder import embed_text

_client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)


def retrieve(question: str, top_k: int = 5) -> list[dict]:
    """Recupera os top_k chunks mais similares a pergunta."""
    query_vector = embed_text(question)
    results = _client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        limit=top_k,
    ).points

    return [
        {"text": r.payload.get("text", ""), "score": r.score, "metadata": r.payload}
        for r in results
    ]
