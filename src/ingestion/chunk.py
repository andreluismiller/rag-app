"""Chunking de documentos por numero de caracteres, com sobreposicao."""

from __future__ import annotations

from typing import Any


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    """Divide um texto em pedacos (chunks) de tamanho fixo com sobreposicao."""
    if chunk_size <= overlap:
        raise ValueError("chunk_size deve ser maior que overlap")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def chunk_documents(
    docs: list[dict[str, Any]], chunk_size: int = 1000, overlap: int = 150
) -> list[dict[str, Any]]:
    """Aplica chunking a uma lista de documentos, preservando metadados e origem."""
    chunked: list[dict[str, Any]] = []
    for doc in docs:
        pieces = chunk_text(doc["text"], chunk_size=chunk_size, overlap=overlap)
        for idx, piece in enumerate(pieces):
            chunked.append(
                {
                    "id": f"{doc['id']}-{idx}",
                    "text": piece,
                    "metadata": {
                        **doc.get("metadata", {}),
                        "source_id": doc["id"],
                        "chunk_index": idx,
                    },
                }
            )
    return chunked
