"""Geracao de embeddings via API da OpenAI.

NOTA: modulo temporario/fase futura. A ingestao (fase 1) usara FastEmbed
(embeddings locais via ONNX, denso + esparso), sem dependencia da OpenAI.
Este arquivo sera usado quando reativarmos geracao de resposta via LLM.
"""

from __future__ import annotations

from openai import OpenAI

from src.config import settings

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Instancia o client OpenAI sob demanda (fase 1 nao depende dele)."""
    global _client
    if _client is None:
        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY nao configurada. Necessaria apenas nas fases "
                "futuras (geracao de resposta / embeddings via OpenAI)."
            )
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Gera embeddings para uma lista de textos em batch."""
    response = _get_client().embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]


def embed_text(text: str) -> list[float]:
    """Gera o embedding de um unico texto."""
    return embed_texts([text])[0]
