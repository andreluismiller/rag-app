"""Metricas de avaliacao de retrieval."""

from __future__ import annotations


def hit_rate(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    """1.0 se ao menos um chunk relevante foi recuperado, 0.0 caso contrario."""
    return 1.0 if set(retrieved_ids) & set(relevant_ids) else 0.0


def mean_reciprocal_rank(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    """Reciprocal rank do primeiro chunk relevante encontrado na lista recuperada."""
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0
