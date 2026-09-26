from __future__ import annotations

import json
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs" / "etapa5"
BASELINE_PATH = ROOT / "runs" / "etapa2" / "baseline_20260924_1724" / "metrics.json"
OUTPUT_JSON = RUNS / "stage5d_confirmation_summary.json"
OUTPUT_MD = ROOT / "reports" / "etapa5d_confirmation.md"

RUNS_BY_CANDIDATE = {
    "start512_lr2e5": {
        1: "etapa5c_start512_lr2e5_fold1_20260924_2359_unsandboxed",
        2: "etapa5d_start512_lr2e5_fold2_20260925",
        3: "etapa5d_start512_lr2e5_fold3_20260925_resume",
    },
    "headtail256_lr2e5": {
        1: "etapa5c_headtail256_lr2e5_fold1_20260925_resume",
        2: "etapa5d_headtail256_lr2e5_fold2_20260925",
        3: "etapa5d_headtail256_lr2e5_fold3_20260925_resume",
    },
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean_sd(values: list[float]) -> tuple[float, float]:
    return statistics.mean(values), statistics.stdev(values)


def pct(value: float) -> str:
    return f"{100 * value:.3f}%"


def pp(value: float) -> str:
    return f"{100 * value:+.3f} pp"


def main() -> None:
    baseline = read_json(BASELINE_PATH)
    baseline_by_fold = {
        fold["fold"]: next(
            candidate["validation"]
            for candidate in fold["candidates"]
            if candidate["C"] == 0.5
        )
        for fold in baseline["folds"]
    }

    candidates: dict[str, dict] = {}
    for candidate_id, fold_runs in RUNS_BY_CANDIDATE.items():
        folds = {}
        for fold_id, run_id in fold_runs.items():
            metrics = read_json(RUNS / run_id / "metrics.json")
            if metrics["candidate"]["id"] != candidate_id:
                raise ValueError(f"Candidato inesperado em {run_id}")
            if metrics["source_sha256"] != baseline["source_sha256"]:
                raise ValueError(f"Hash de fonte divergente em {run_id}")
            if metrics["split_sha256"] != baseline["split_sha256"]:
                raise ValueError(f"Hash de divisão divergente em {run_id}")
            if metrics["config"]["fold"] != fold_id:
                raise ValueError(f"Fold inesperado em {run_id}")
            if metrics["holdout_evaluated"]:
                raise ValueError(f"Holdout marcado como avaliado em {run_id}")
            if not metrics["checkpoint_reload"]["all_finite"]:
                raise ValueError(f"Checkpoint inválido em {run_id}")
            folds[fold_id] = {
                "run_id": run_id,
                "train_rows": metrics["train_rows"],
                "validation_rows": metrics["validation_rows"],
                "accuracy": metrics["best_validation_accuracy"],
                "macro_f1": metrics["best_validation_macro_f1"],
                "best_step": metrics["best_optimizer_step"],
                "completed_steps": metrics["completed_optimizer_steps"],
                "completed_epochs": metrics["completed_epochs"],
                "early_stopped": metrics["early_stopped"],
                "total_wall_seconds": metrics["total_wall_seconds"],
                "peak_allocated_bytes": metrics["gpu"]["peak_allocated_bytes"],
                "checkpoint_reload": metrics["checkpoint_reload"],
                "baseline_accuracy": baseline_by_fold[fold_id]["accuracy"],
                "baseline_macro_f1": baseline_by_fold[fold_id]["macro_f1"],
            }
        acc_mean, acc_sd = mean_sd([f["accuracy"] for f in folds.values()])
        f1_mean, f1_sd = mean_sd([f["macro_f1"] for f in folds.values()])
        candidates[candidate_id] = {
            "folds": folds,
            "accuracy_mean": acc_mean,
            "accuracy_sample_sd": acc_sd,
            "macro_f1_mean": f1_mean,
            "macro_f1_sample_sd": f1_sd,
            "mean_wall_seconds": statistics.mean(
                f["total_wall_seconds"] for f in folds.values()
            ),
        }

    baseline_acc_mean, baseline_acc_sd = mean_sd(
        [baseline_by_fold[i]["accuracy"] for i in (1, 2, 3)]
    )
    baseline_f1_mean, baseline_f1_sd = mean_sd(
        [baseline_by_fold[i]["macro_f1"] for i in (1, 2, 3)]
    )
    summary = {
        "stage": "5d",
        "split_id": baseline["split_id"],
        "source_sha256": baseline["source_sha256"],
        "split_sha256": baseline["split_sha256"],
        "baseline": {
            "run_id": baseline["run_id"],
            "C": 0.5,
            "accuracy_mean": baseline_acc_mean,
            "accuracy_sample_sd": baseline_acc_sd,
            "macro_f1_mean": baseline_f1_mean,
            "macro_f1_sample_sd": baseline_f1_sd,
            "folds": baseline_by_fold,
        },
        "candidates": candidates,
        "selection_rule": "mean fold validation accuracy; macro-F1 as tie-breaker",
        "selected_by_primary_metric": max(
            candidates,
            key=lambda cid: candidates[cid]["accuracy_mean"],
        ),
        "holdout_evaluated": False,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Etapa 5d — Confirmação dos finalistas nos folds 2 e 3",
        "",
        "**Status:** concluída. Política de dados: Original. O holdout não foi consultado.",
        "",
        "## Protocolo",
        "",
        "Foram reutilizadas as corridas completas do fold 1 (5c) e reunidas às quatro corridas novas dos folds 2 e 3. Cada corrida usa até duas épocas, lote efetivo 8, validação completa a cada 384 passos e no fim de cada época, acurácia para selecionar checkpoint e macro-F1 como desempate. TF-IDF `C=0,5` vem da avaliação pareada da Etapa 2. Os folds são agrupados por texto e não compartilham grupos entre treino e validação.",
        "",
        "## Resultados por fold",
        "",
        "| Candidato | Fold | Acurácia | Macro-F1 | Baseline TF-IDF acc. | Δ acc. | Tempo (min) | Passo melhor |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for candidate_id, candidate in candidates.items():
        for fold_id, fold in candidate["folds"].items():
            lines.append(
                f"| `{candidate_id}` | {fold_id} | {pct(fold['accuracy'])} | {pct(fold['macro_f1'])} | {pct(fold['baseline_accuracy'])} | {pp(fold['accuracy'] - fold['baseline_accuracy'])} | {fold['total_wall_seconds'] / 60:.2f} | {fold['best_step']} |"
            )
    lines += [
        "",
        "## Média entre os três folds",
        "",
        "| Modelo | Acurácia média ± DP amostral | Macro-F1 média ± DP amostral | Tempo médio por corrida |",
        "|---|---:|---:|---:|",
    ]
    for name, stats in [
        ("TF-IDF `C=0,5`", summary["baseline"]),
        *candidates.items(),
    ]:
        display_name = name if name.startswith("TF-IDF") else f"`{name}`"
        mean_time = (
            "—" if name.startswith("TF-IDF") else f"{stats['mean_wall_seconds'] / 60:.2f} min"
        )
        lines.append(
            f"| {display_name} | {pct(stats['accuracy_mean'])} ± {pct(stats['accuracy_sample_sd'])} | {pct(stats['macro_f1_mean'])} ± {pct(stats['macro_f1_sample_sd'])} | {mean_time} |"
        )
    start = candidates["start512_lr2e5"]
    headtail = candidates["headtail256_lr2e5"]
    delta_acc = start["accuracy_mean"] - headtail["accuracy_mean"]
    delta_f1 = start["macro_f1_mean"] - headtail["macro_f1_mean"]
    lines += [
        "",
        "## Decisão da 5d",
        "",
        f"Pelo critério primário congelado, `start512_lr2e5` fica como referência: sua acurácia média é maior por {pp(delta_acc)}. `headtail256_lr2e5` tem macro-F1 médio maior por {pp(-delta_f1)} e tempo médio menor. As diferenças são pequenas frente à variação observada entre folds; a escolha do checkpoint principal segue a acurácia, sem inferência de superioridade estatística.",
        "",
        f"Ambos os candidatos superam o TF-IDF em acurácia média por {pp(start['accuracy_mean'] - baseline_acc_mean)} (`start512_lr2e5`) e {pp(headtail['accuracy_mean'] - baseline_acc_mean)} (`headtail256_lr2e5`). A 5d confirma apenas o protocolo/folds observados; ainda não fixa a política final nem autoriza consulta ao holdout.",
        "",
        "## Artefatos e integridade",
        "",
        f"Resumo de máquina: `runs/etapa5/{OUTPUT_JSON.name}`. O script `src/summarize_stage5d.py` carrega IDs e métricas persistidos, confirma candidato/fold e recarga de checkpoint, e exige que o holdout esteja marcado como não avaliado. Hashes da fonte e divisão: `{baseline['source_sha256']}` e `{baseline['split_sha256']}`. Nenhum rótulo, split ou conjunto de holdout foi alterado.",
    ]
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Resumo salvo em {OUTPUT_JSON}")
    print(f"Relatório salvo em {OUTPUT_MD}")
    print(f"Seleção pela métrica primária: {summary['selected_by_primary_metric']}")


if __name__ == "__main__":
    main()
