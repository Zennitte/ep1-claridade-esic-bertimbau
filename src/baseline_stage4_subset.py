"""Aplica o baseline TF-IDF fixado à mesma amostra da triagem BERT."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from threadpoolctl import threadpool_limits

from audit_and_split import digest_file
from experiment_metrics import classification_metrics
from run_baseline import load_data


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / "configs" / "baseline.json").read_text(encoding="utf-8"))
    split_path = root / "data" / "splits_grouped_v1.json"
    split = json.loads(split_path.read_text(encoding="utf-8"))
    subset_path = root / "data" / "stage4_subset.json"
    subset = json.loads(subset_path.read_text(encoding="utf-8"))
    if subset["split_sha256"] != digest_file(split_path):
        raise ValueError("A amostra não corresponde à divisão congelada")
    texts, labels = load_data(root, split)
    train = np.array(subset["train"])
    valid = np.array(subset["validation"])
    assert not set(train).intersection(valid)
    selected_c = 0.5  # valor escolhido nos três folds completos da Etapa 2
    vector_config = dict(config["vectorizer"])
    vector_config["ngram_range"] = tuple(vector_config["ngram_range"])
    started = time.perf_counter()
    with threadpool_limits(limits=config["cpu_threads"]):
        vectorizer = TfidfVectorizer(**vector_config)
        x_train = vectorizer.fit_transform(texts[train])
        x_valid = vectorizer.transform(texts[valid])
        model = LogisticRegression(
            C=selected_c, solver=config["classifier"]["solver"],
            max_iter=config["classifier"]["max_iter"], random_state=config["seed"],
        ).fit(x_train, labels[train])
        train_pred = model.predict(x_train)
        valid_pred = model.predict(x_valid)
    checkpoint = root / "models" / "baseline" / "stage4_subset_c0_5.joblib"
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(Pipeline([("tfidf", vectorizer), ("logreg", model)]), checkpoint, compress=3)
    result = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": split["source_sha256"],
        "split_id": split["id"],
        "subset_id": subset["id"],
        "subset_sha256": digest_file(subset_path),
        "C": selected_c,
        "train_rows": len(train),
        "validation_rows": len(valid),
        "train": classification_metrics(labels[train], train_pred, config["classes"]),
        "validation": classification_metrics(labels[valid], valid_pred, config["classes"]),
        "vocabulary_size": len(vectorizer.vocabulary_),
        "wall_seconds": round(time.perf_counter() - started, 3),
        "checkpoint": str(checkpoint.relative_to(root)),
        "holdout_evaluated": False,
    }
    output = root / "runs" / "etapa4" / "baseline_same_subset.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"validation": result["validation"], "wall_seconds": result["wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
