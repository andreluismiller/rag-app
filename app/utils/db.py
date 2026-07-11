"""Acesso ao Postgres: registra interacoes/feedback e alimenta o dashboard."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd
import psycopg
from psycopg.rows import dict_row

from src.config import settings


def get_connection() -> psycopg.Connection:
    return psycopg.connect(settings.postgres_dsn, row_factory=dict_row)


def save_interaction(result: dict[str, Any]) -> int:
    """Persiste uma interacao (pergunta/resposta) e retorna o id gerado."""
    usage = result.get("usage", {})
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO interactions
                (session_id, question, answer, retrieved_chunks, model,
                 latency_ms, prompt_tokens, completion_tokens, total_tokens)
            VALUES (%(session_id)s, %(question)s, %(answer)s, %(retrieved_chunks)s, %(model)s,
                    %(latency_ms)s, %(prompt_tokens)s, %(completion_tokens)s, %(total_tokens)s)
            RETURNING id
            """,
            {
                "session_id": result.get("session_id"),
                "question": result["question"],
                "answer": result["answer"],
                "retrieved_chunks": json.dumps(result.get("retrieved_chunks", [])),
                "model": settings.openai_chat_model,
                "latency_ms": result.get("latency_ms"),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
            },
        )
        return cur.fetchone()["id"]


def save_feedback(interaction_id: int, rating: int, comment: str | None = None) -> None:
    """Persiste o feedback do usuario (1 para positivo, -1 para negativo)."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO feedback (interaction_id, rating, comment) VALUES (%s, %s, %s)",
            (interaction_id, rating, comment),
        )


def fetch_interactions(limit: int = 500) -> pd.DataFrame:
    """Retorna as interacoes mais recentes, para uso no dashboard."""
    with get_connection() as conn:
        return pd.read_sql(
            """
            SELECT i.*, f.rating, f.comment AS feedback_comment
            FROM interactions i
            LEFT JOIN feedback f ON f.interaction_id = i.id
            ORDER BY i.created_at DESC
            LIMIT %(limit)s
            """,
            conn,
            params={"limit": limit},
        )
