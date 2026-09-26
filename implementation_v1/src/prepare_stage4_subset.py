"""Congela uma amostra estratificada dentro do fold 1 para a triagem da Etapa 4."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from audit_and_split import digest_file
from bert_stage3 import read_dataset


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / "configs" / "bert_stage4.json").read_text(encoding="utf-8"))
    split_path = root / "data" / "splits_grouped_v1.json"
    split = json.loads(split_path.read_text(encoding="utf-8"))
    if config["split_id"] != split["id"]:
        raise ValueError("Configuração e divisão não correspondem")
    _, labels = read_dataset(root, split)
    labels = np.array(labels)
    fold = next(item for item in split["folds"] if item["fold"] == config["fold"])
    train, _ = train_test_split(
        fold["train"], train_size=config["train_rows"],
        stratify=labels[fold["train"]], random_state=config["seed"],
    )
    validation, _ = train_test_split(
        fold["validation"], train_size=config["validation_rows"],
        stratify=labels[fold["validation"]], random_state=config["seed"] + 1,
    )
    train = sorted(map(int, train))
    validation = sorted(map(int, validation))
    holdout = set(split["holdout"])
    assert not set(train).intersection(validation)
    assert not set(train).intersection(holdout)
    assert not set(validation).intersection(holdout)
    manifest = {
        "id": "stage4_fold1_stratified_4096_1024_seed_20260924",
        "source_sha256": split["source_sha256"],
        "split_id": split["id"],
        "split_sha256": digest_file(split_path),
        "seed": config["seed"],
        "fold": config["fold"],
        "indexing": "zero-based data rows; Excel row = index + 2",
        "method": "train_test_split separately within fold train and validation, stratified by original label",
        "train": train,
        "validation": validation,
        "train_counts": dict(Counter(labels[train])),
        "validation_counts": dict(Counter(labels[validation])),
    }
    output = root / "data" / "stage4_subset.json"
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
        if existing != manifest:
            raise ValueError("O subconjunto já existe com conteúdo diferente")
    else:
        output.write_text(json.dumps(manifest, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in manifest.items() if key not in ("train", "validation")}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
