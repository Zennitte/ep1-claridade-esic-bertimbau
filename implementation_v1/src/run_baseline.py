"""Executa classe majoritária e TF-IDF + regressão logística nos folds fixados."""

from __future__ import annotations

import argparse
import json
import platform
import time
import warnings
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import joblib
import numpy as np
import openpyxl
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from threadpoolctl import threadpool_limits

from audit_and_split import digest_file
from experiment_metrics import classification_metrics
from plot_curves import plot_series_svg


def load_data(root: Path, split: dict) -> tuple[np.ndarray, np.ndarray]:
    source = root / split["source"]
    if digest_file(source) != split["source_sha256"]:
        raise ValueError("Hash de train.xlsx difere do arquivo usado na divisão")
    workbook = openpyxl.load_workbook(source, read_only=True, data_only=True)
    sheet = workbook["train"]
    if tuple(cell.value for cell in sheet[1]) != ("resp_text", "clarity"):
        raise ValueError("Cabeçalho inesperado")
    records = list(sheet.iter_rows(min_row=2, max_col=2, values_only=True))
    workbook.close()
    text = np.array([value if isinstance(value, str) else str(value) for value, _ in records], dtype=object)
    labels = np.array([label for _, label in records])
    return text, labels


def run(root: Path, run_id: str) -> dict:
    started = time.perf_counter()
    config_path = root / "configs" / "baseline.json"
    split_path = root / "data" / "splits_grouped_v1.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    split = json.loads(split_path.read_text(encoding="utf-8"))
    if split["id"] != config["split_id"]:
        raise ValueError("Configuração e divisão não correspondem")
    texts, labels = load_data(root, split)
    classes = config["classes"]
    run_dir = root / "runs" / "etapa2" / run_id
    model_dir = root / "models" / "baseline" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    model_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    results = {
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": split["source_sha256"],
        "split_id": split["id"],
        "split_sha256": digest_file(split_path),
        "config": config,
        "versions": {name: version(name) for name in ("scikit-learn", "numpy", "openpyxl", "joblib")},
        "platform": platform.platform(),
        "gpu_used": False,
        "holdout_evaluated": False,
        "folds": [],
    }
    vector_config = dict(config["vectorizer"])
    vector_config["ngram_range"] = tuple(vector_config["ngram_range"])
    with threadpool_limits(limits=config["cpu_threads"]):
        for fold in split["folds"]:
            fold_number = fold["fold"]
            train_indices = np.array(fold["train"])
            valid_indices = np.array(fold["validation"])
            assert set(train_indices).isdisjoint(valid_indices)
            assert set(train_indices).isdisjoint(split["holdout"])
            assert set(valid_indices).isdisjoint(split["holdout"])
            train_text, valid_text = texts[train_indices], texts[valid_indices]
            y_train, y_valid = labels[train_indices], labels[valid_indices]
            majority = Counter(y_train).most_common(1)[0][0]
            majority_train = classification_metrics(y_train, np.full(len(y_train), majority), classes)
            majority_valid = classification_metrics(y_valid, np.full(len(y_valid), majority), classes)
            fold_result = {
                "fold": fold_number,
                "train_rows": len(train_indices),
                "validation_rows": len(valid_indices),
                "majority": {"label": majority, "train": majority_train, "validation": majority_valid},
                "candidates": [],
            }

            vectorizer = TfidfVectorizer(**vector_config)
            vector_start = time.perf_counter()
            x_train = vectorizer.fit_transform(train_text)
            x_valid = vectorizer.transform(valid_text)
            vector_seconds = time.perf_counter() - vector_start
            fold_result["vectorizer"] = {
                "fit_and_transform_seconds": round(vector_seconds, 3),
                "vocabulary_size": len(vectorizer.vocabulary_),
                "train_nonzero": int(x_train.nnz),
                "validation_nonzero": int(x_valid.nnz),
            }

            for c_value in config["classifier"]["C_values"]:
                clf = LogisticRegression(
                    C=c_value,
                    solver=config["classifier"]["solver"],
                    max_iter=config["classifier"]["max_iter"],
                    random_state=config["seed"],
                )
                fit_start = time.perf_counter()
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always", ConvergenceWarning)
                    clf.fit(x_train, y_train)
                fit_seconds = time.perf_counter() - fit_start
                predict_start = time.perf_counter()
                train_pred = clf.predict(x_train)
                valid_pred = clf.predict(x_valid)
                predict_seconds = time.perf_counter() - predict_start
                checkpoint = model_dir / f"fold_{fold_number}_c_{str(c_value).replace('.', '_')}.joblib"
                checkpoint_start = time.perf_counter()
                joblib.dump(Pipeline([("tfidf", vectorizer), ("logreg", clf)]), checkpoint, compress=3)
                save_seconds = time.perf_counter() - checkpoint_start
                fold_result["candidates"].append(
                    {
                        "C": c_value,
                        "train": classification_metrics(y_train, train_pred, classes),
                        "validation": classification_metrics(y_valid, valid_pred, classes),
                        "classifier_fit_seconds": round(fit_seconds, 3),
                        "prediction_seconds": round(predict_seconds, 3),
                        "checkpoint_save_seconds": round(save_seconds, 3),
                        "checkpoint": str(checkpoint.relative_to(root)),
                        "iterations": int(np.max(clf.n_iter_)),
                        "warnings": [str(item.message) for item in caught],
                    }
                )
                print(
                    f"fold={fold_number} C={c_value} "
                    f"train={fold_result['candidates'][-1]['train']['accuracy']:.4f} "
                    f"valid={fold_result['candidates'][-1]['validation']['accuracy']:.4f} "
                    f"fit_s={fit_seconds:.2f}",
                    flush=True,
                )
            results["folds"].append(fold_result)
            (run_dir / "metrics_partial.json").write_text(
                json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )

    summaries = []
    for c_value in config["classifier"]["C_values"]:
        values = [
            next(item for item in fold["candidates"] if item["C"] == c_value)
            for fold in results["folds"]
        ]
        summaries.append(
            {
                "C": c_value,
                "mean_accuracy": float(np.mean([item["validation"]["accuracy"] for item in values])),
                "std_accuracy": float(np.std([item["validation"]["accuracy"] for item in values], ddof=1)),
                "mean_macro_f1": float(np.mean([item["validation"]["macro_f1"] for item in values])),
                "mean_train_accuracy": float(np.mean([item["train"]["accuracy"] for item in values])),
                "total_classifier_fit_seconds": round(sum(item["classifier_fit_seconds"] for item in values), 3),
            }
        )
    majority_values = [fold["majority"]["validation"] for fold in results["folds"]]
    results["summary"] = {
        "majority_mean_accuracy": float(np.mean([item["accuracy"] for item in majority_values])),
        "majority_mean_macro_f1": float(np.mean([item["macro_f1"] for item in majority_values])),
        "candidates": summaries,
        "selected_C_by_mean_validation_accuracy": max(
            summaries, key=lambda item: (item["mean_accuracy"], item["mean_macro_f1"], -item["C"])
        )["C"],
    }
    results["total_wall_seconds"] = round(time.perf_counter() - started, 3)
    (run_dir / "metrics.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    curve = {
        "title": "Baseline TF-IDF: acurácia por regularização",
        "x_label": "C da regressão logística",
        "y_label": "Acurácia",
        "series": [
            {
                "label": f"Validação fold {fold['fold']}",
                "points": [[item["C"], item["validation"]["accuracy"]] for item in fold["candidates"]],
            }
            for fold in results["folds"]
        ]
        + [
            {
                "label": "Média validação",
                "points": [[item["C"], item["mean_accuracy"]] for item in summaries],
            }
        ],
    }
    (run_dir / "curve.json").write_text(json.dumps(curve, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plot_series_svg(curve, root / "reports" / "etapa2_baseline_curve.svg")
    print(json.dumps({"run_id": run_id, "summary": results["summary"], "wall_seconds": results["total_wall_seconds"]}, indent=2))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    run_id = args.run_id or datetime.now().strftime("baseline_%Y%m%d_%H%M%S")
    run(Path(__file__).resolve().parents[1], run_id)


if __name__ == "__main__":
    main()
