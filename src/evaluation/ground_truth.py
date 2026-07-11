"""Carregamento do conjunto de perguntas de ground truth para avaliacao."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

GROUND_TRUTH_DIR = Path("data/ground_truth")


def load_ground_truth(filename: str = "questions.json") -> list[dict[str, Any]]:
    """Carrega perguntas de ground truth.

    Formato esperado (lista de objetos):
        {"question": "...", "expected_answer": "...", "relevant_chunk_ids": ["..."]}
    """
    path = GROUND_TRUTH_DIR / filename
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
