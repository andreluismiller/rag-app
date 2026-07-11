"""Orquestra retrieval + generation para responder uma pergunta do usuario."""

from __future__ import annotations

import time
from typing import Any

from src.rag.generator import generate_answer
from src.rag.retriever import retrieve


def answer_question(question: str, top_k: int = 5) -> dict[str, Any]:
    """Executa o fluxo RAG completo para uma pergunta e retorna resposta + metadados."""
    start = time.perf_counter()

    chunks = retrieve(question, top_k=top_k)
    answer, usage = generate_answer(question, chunks)

    latency_ms = int((time.perf_counter() - start) * 1000)

    return {
        "question": question,
        "answer": answer,
        "retrieved_chunks": chunks,
        "usage": usage,
        "latency_ms": latency_ms,
    }
