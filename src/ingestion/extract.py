"""Extracao de documentos brutos a partir de arquivos JSON e CSV em data/raw."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

RAW_DIR = Path("data/raw")


def load_json_documents(path: Path) -> list[dict[str, Any]]:
    """Carrega uma lista de documentos a partir de um arquivo JSON.

    Formato esperado: lista de objetos, cada um com ao menos "id" e "text".
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def load_csv_documents(
    path: Path, text_column: str = "text", id_column: str | None = None
) -> list[dict[str, Any]]:
    """Carrega documentos a partir de um arquivo CSV."""
    docs = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            docs.append(
                {
                    "id": row[id_column] if id_column else str(i),
                    "text": row[text_column],
                    "metadata": {
                        k: v for k, v in row.items() if k not in (text_column, id_column)
                    },
                }
            )
    return docs


def load_all_documents(raw_dir: Path = RAW_DIR) -> list[dict[str, Any]]:
    """Percorre data/raw e carrega todos os documentos JSON e CSV encontrados."""
    docs: list[dict[str, Any]] = []
    for path in sorted(raw_dir.glob("*.json")):
        docs.extend(load_json_documents(path))
    for path in sorted(raw_dir.glob("*.csv")):
        docs.extend(load_csv_documents(path))
    return docs
