"""Consolida a triagem da Etapa 4 e produz a curva comparativa."""

from __future__ import annotations

import json
from pathlib import Path

from plot_curves import plot_series_svg


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs" / "etapa4"
REPORTS = ROOT / "reports" / "etapa4"
ORDER = (
    "start512_lr2e5",
    "headtail256_lr2e5",
    "start256_lr2e5",
    "start256_lr3e5",
    "headtail256_lr3e5",
    "headtail512_lr2e5",
    "start512_lr3e5",
    "headtail512_lr3e5",
)
LABELS = {
    "start512_lr2e5": "inicio 2e-5",
    "headtail256_lr2e5": "início+fim 2e-5",
    "start256_lr2e5": "início 2e-5",
    "start256_lr3e5": "início 3e-5",
    "headtail256_lr3e5": "início+fim 3e-5",
    "headtail512_lr2e5": "início+fim 2e-5",
    "start512_lr3e5": "início 3e-5",
    "headtail512_lr3e5": "início+fim 3e-5",
}


def main() -> None:
    baseline = json.loads((RUNS / "baseline_same_subset.json").read_text(encoding="utf-8"))
    baseline_accuracy = baseline["validation"]["accuracy"]
    series_by_length = {256: [], 512: []}
    summary = []
    subset_ids = {baseline["subset_id"]}
    for candidate_id in ORDER:
        paths = list(RUNS.glob(f"stage4_{candidate_id}_*/metrics.json"))
        if len(paths) != 1:
            raise ValueError(f"Esperado um resultado para {candidate_id}; encontrados {len(paths)}")
        metrics = json.loads(paths[0].read_text(encoding="utf-8"))
        if metrics["candidate"]["id"] != candidate_id or metrics["holdout_evaluated"]:
            raise ValueError(f"Metadados inconsistentes em {paths[0]}")
        subset_ids.add(metrics["subset_id"])
        series_by_length[metrics["candidate"]["max_length"]].append({
            "label": LABELS[candidate_id],
            "points": [
                [row["optimizer_step"], row["validation"]["metrics"]["accuracy"]]
                for row in metrics["history"]
            ],
        })
        summary.append({
            "candidate_id": candidate_id,
            "run_id": metrics["run_id"],
            "best_step": metrics["best_optimizer_step"],
            "best_accuracy": metrics["best_validation_accuracy"],
            "best_macro_f1": metrics["best_validation_macro_f1"],
            "delta_baseline_percentage_points": 100 * (metrics["best_validation_accuracy"] - baseline_accuracy),
            "wall_seconds": metrics["total_wall_seconds"],
            "peak_allocated_bytes": metrics["gpu"]["peak_allocated_bytes"],
            "validation_truncated_rows": metrics["validation_token_stats"]["truncated_rows"],
        })
    if len(subset_ids) != 1:
        raise ValueError(f"Subconjuntos diferentes: {subset_ids}")
    REPORTS.mkdir(parents=True, exist_ok=True)
    for max_length, series in series_by_length.items():
        series.append({"label": "TF-IDF C=0,5", "points": [[128, baseline_accuracy], [1024, baseline_accuracy]]})
        plot_series_svg({
            "title": f"Etapa 4: janela {max_length}, acuracia (n=1024)",
            "x_label": "Passo do otimizador",
            "y_label": "Acurácia",
            "series": series,
        }, REPORTS / f"comparison_accuracy_{max_length}.svg")
    (REPORTS / "comparison_summary.json").write_text(
        json.dumps({"subset_id": subset_ids.pop(), "baseline_accuracy": baseline_accuracy, "candidates": summary},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
