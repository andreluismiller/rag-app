"""Script de avaliacao do retrieval contra o ground truth.

Uso:
    uv run python -m src.evaluation.run_eval
"""

from __future__ import annotations

from src.evaluation.ground_truth import load_ground_truth
from src.evaluation.metrics import hit_rate, mean_reciprocal_rank
from src.rag.retriever import retrieve


def run() -> None:
    dataset = load_ground_truth()
    hit_rates, mrrs = [], []

    for item in dataset:
        results = retrieve(item["question"], top_k=5)
        retrieved_ids = [r["metadata"].get("source_id", "") for r in results]
        relevant_ids = item.get("relevant_chunk_ids", [])

        hit_rates.append(hit_rate(retrieved_ids, relevant_ids))
        mrrs.append(mean_reciprocal_rank(retrieved_ids, relevant_ids))

    print(f"Perguntas avaliadas: {len(dataset)}")
    print(f"Hit Rate medio: {sum(hit_rates) / len(hit_rates):.3f}")
    print(f"MRR medio: {sum(mrrs) / len(mrrs):.3f}")


if __name__ == "__main__":
    run()
