"""Geracao da resposta final a partir do contexto recuperado.

NOTA: modulo de fase futura (chat com LLM). Nao e usado na ingestao (fase 1).
"""

from __future__ import annotations

from openai import OpenAI

from src.config import settings

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY nao configurada.")
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client

SYSTEM_PROMPT = (
    "Voce e um assistente que responde perguntas com base apenas no contexto fornecido. "
    "Se a resposta nao estiver no contexto, diga que nao sabe."
)


def generate_answer(question: str, context_chunks: list[dict]) -> tuple[str, dict]:
    """Gera a resposta final e retorna tambem metadados de uso (tokens, etc.)."""
    context = "\n\n".join(c["text"] for c in context_chunks)
    user_prompt = f"Contexto:\n{context}\n\nPergunta: {question}"

    response = _get_client().chat.completions.create(
        model=settings.openai_chat_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    answer = response.choices[0].message.content or ""
    usage = {
        "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
        "completion_tokens": response.usage.completion_tokens if response.usage else None,
        "total_tokens": response.usage.total_tokens if response.usage else None,
    }
    return answer, usage
