"""Gera e valida manifests de treino A/B/C para a ablação 5c.1."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from audit_and_split import digest_file


LABELS = ("c1", "c234", "c5")
VARIANT_FILES = {
    "A_original": "fold1_original.json",
    "B_remove_conflicts": "fold1_remove_conflicts.json",
    "C_majority_conflicts": "fold1_majority_conflicts.json",
}


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_row_manifest(path: Path) -> tuple[dict[int, dict], str]:
    rows: dict[int, dict] = {}
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            index = int(row["row_index"])
            if index in rows:
                raise AssertionError(f"row_index duplicado no manifesto: {index}")
            rows[index] = {
                "group_id": row["group_sha256"],
                "label": row["clarity"],
                "excel_row": int(row["excel_row"]),
            }
    return rows, digest_file(path)


def validate_all(root: Path, *, require_manifests: bool = True) -> dict:
    config = json.loads((root / "configs/bert_stage5_conflict_ablation.json").read_text(encoding="utf-8"))
    split_path = root / config["split"]["path"]
    split = json.loads(split_path.read_text(encoding="utf-8"))
    row_path = root / config["row_manifest"]["path"]
    rows, row_hash = load_row_manifest(row_path)
    source_path = root / config["source"]["path"]
    source_hash = digest_file(source_path)
    split_hash = digest_file(split_path)

    assert source_hash == config["source"]["sha256"] == split["source_sha256"]
    assert split_hash == config["split"]["sha256"]
    assert row_hash == config["row_manifest"]["sha256"]
    assert split["id"] == config["split"]["id"]
    assert set(rows) == set(range(len(rows)))
    assert set(row["label"] for row in rows.values()) == set(LABELS)

    fold = next(item for item in split["folds"] if item["fold"] == 1)
    original_train = list(fold["train"])
    validation = list(fold["validation"])
    holdout = list(split["holdout"])
    assert len(original_train) == config["split"]["train_rows"] == len(set(original_train))
    assert len(validation) == config["split"]["validation_rows"] == len(set(validation))
    assert not set(original_train) & set(validation)
    assert not set(original_train) & set(holdout)
    assert not set(validation) & set(holdout)
    assert all(index in rows for index in original_train + validation + holdout)

    # Use only the frozen Etapa 1 group IDs and the labels on this fold's train rows.
    train_groups: dict[str, list[int]] = defaultdict(list)
    for index in original_train:
        train_groups[rows[index]["group_id"]].append(index)
    conflicts = {
        group_id: indices
        for group_id, indices in train_groups.items()
        if len({rows[index]["label"] for index in indices}) > 1
    }
    group_audit = {}
    keep_b = set(original_train)
    keep_c = set(original_train)
    for group_id, indices in conflicts.items():
        counts = Counter(rows[index]["label"] for index in indices)
        high = max(counts.values())
        winners = [label for label, count in counts.items() if count == high]
        group_audit[group_id] = {
            "indices": sorted(indices),
            "label_counts": {label: counts[label] for label in LABELS if counts[label]},
            "unique_majority_label": winners[0] if len(winners) == 1 else None,
            "tied": len(winners) > 1,
        }
        keep_b.difference_update(indices)
        if len(winners) > 1:
            keep_c.difference_update(indices)
        else:
            keep_c.difference_update(index for index in indices if rows[index]["label"] != winners[0])

    variant_keep = {
        "A_original": set(original_train),
        "B_remove_conflicts": keep_b,
        "C_majority_conflicts": keep_c,
    }
    if require_manifests:
        manifest_dir = root / "data/stage5_conflict_ablation"
        for variant, filename in VARIANT_FILES.items():
            path = manifest_dir / filename
            if not path.is_file():
                raise AssertionError(f"Manifest ausente: {path}")
            manifest = json.loads(path.read_text(encoding="utf-8"))
            assert manifest["variant_id"] == variant
            assert manifest["source_sha256"] == source_hash
            assert manifest["split_sha256"] == split_hash
            assert manifest["row_manifest_sha256"] == row_hash
            assert manifest["fold"] == 1 and manifest["seed"] == config["fixed_training_protocol"]["seed"]
            assert manifest["original_train_indices"] == original_train
            assert manifest["validation_indices"] == validation
            assert manifest["validation_indices_sha256"] == canonical_hash(validation)
            assert manifest["holdout_indices_sha256"] == canonical_hash(holdout)
            expected_kept = [index for index in original_train if index in variant_keep[variant]]
            expected_removed = [index for index in original_train if index not in variant_keep[variant]]
            assert manifest["retained_train_indices"] == expected_kept
            assert manifest["removed_train_indices"] == expected_removed
            assert manifest["conflicting_groups"] == group_audit

        a = json.loads((manifest_dir / VARIANT_FILES["A_original"]).read_text(encoding="utf-8"))
        b = json.loads((manifest_dir / VARIANT_FILES["B_remove_conflicts"]).read_text(encoding="utf-8"))
        c = json.loads((manifest_dir / VARIANT_FILES["C_majority_conflicts"]).read_text(encoding="utf-8"))
        assert a["retained_train_indices"] == original_train
        assert not (set(b["retained_train_indices"]) & {i for ids in conflicts.values() for i in ids})
        assert set(c["retained_train_indices"]) == keep_c

    # Label, group and partition invariants for all policies.
    for variant, kept in variant_keep.items():
        assert kept <= set(original_train)
        assert len(kept) == len(list(kept))
        assert set(rows[i]["label"] for i in kept) == set(LABELS)
        for index in kept:
            assert rows[index]["label"] in LABELS
        remaining_by_group: dict[str, set[str]] = defaultdict(set)
        for index in kept:
            remaining_by_group[rows[index]["group_id"]].add(rows[index]["label"])
        if variant == "B_remove_conflicts":
            assert not any(group_id in conflicts for group_id in remaining_by_group)
        if variant == "C_majority_conflicts":
            assert all(len(labels) == 1 for labels in remaining_by_group.values())
            assert all(not audit["tied"] for group_id, audit in group_audit.items() if group_id in remaining_by_group)
            assert all(rows[i]["label"] in {rows[j]["label"] for j in train_groups[rows[i]["group_id"]]} for i in kept)

    # Group isolation must still hold for the untouched validation set.
    train_group_ids = {rows[i]["group_id"] for i in original_train}
    val_group_ids = {rows[i]["group_id"] for i in validation}
    assert not train_group_ids & val_group_ids
    assert validation == list(fold["validation"])
    assert holdout == list(split["holdout"])

    counts = {}
    for variant, kept in variant_keep.items():
        label_counts = Counter(rows[index]["label"] for index in kept)
        counts[variant] = {"rows": len(kept), "class_counts": {label: label_counts[label] for label in LABELS}}
    return {
        "source_sha256": source_hash,
        "split_sha256": split_hash,
        "row_manifest_sha256": row_hash,
        "fold": 1,
        "train_rows": len(original_train),
        "validation_rows": len(validation),
        "holdout_rows": len(holdout),
        "conflicting_groups": len(conflicts),
        "conflicting_rows": sum(map(len, conflicts.values())),
        "unique_majority_groups": sum(not item["tied"] for item in group_audit.values()),
        "tied_groups": sum(item["tied"] for item in group_audit.values()),
        "variants": counts,
        "assertions": "passed",
    }


def create_manifests(root: Path) -> dict:
    config = json.loads((root / "configs/bert_stage5_conflict_ablation.json").read_text(encoding="utf-8"))
    split_path = root / config["split"]["path"]
    split = json.loads(split_path.read_text(encoding="utf-8"))
    rows, row_hash = load_row_manifest(root / config["row_manifest"]["path"])
    source_hash = digest_file(root / config["source"]["path"])
    split_hash = digest_file(split_path)
    fold = next(item for item in split["folds"] if item["fold"] == 1)
    original_train = list(fold["train"])
    validation = list(fold["validation"])
    holdout = list(split["holdout"])

    groups: dict[str, list[int]] = defaultdict(list)
    for index in original_train:
        groups[rows[index]["group_id"]].append(index)
    conflict_data = {}
    keep_b = set(original_train)
    keep_c = set(original_train)
    for group_id, indices in groups.items():
        counts = Counter(rows[index]["label"] for index in indices)
        if len(counts) <= 1:
            continue
        maximum = max(counts.values())
        winners = [label for label, count in counts.items() if count == maximum]
        conflict_data[group_id] = {
            "indices": sorted(indices),
            "label_counts": {label: counts[label] for label in LABELS if counts[label]},
            "unique_majority_label": winners[0] if len(winners) == 1 else None,
            "tied": len(winners) > 1,
        }
        keep_b.difference_update(indices)
        if len(winners) > 1:
            keep_c.difference_update(indices)
        else:
            keep_c.difference_update(index for index in indices if rows[index]["label"] != winners[0])

    kept = {"A_original": set(original_train), "B_remove_conflicts": keep_b, "C_majority_conflicts": keep_c}
    manifest_dir = root / "data/stage5_conflict_ablation"
    manifest_dir.mkdir(parents=True, exist_ok=False)
    generated_utc = datetime.now(timezone.utc).isoformat()
    holdout_hash = canonical_hash(holdout)
    validation_hash = canonical_hash(validation)
    for variant, filename in VARIANT_FILES.items():
        # Preserve split order so the control keeps the exact DataLoader input order.
        keep = [index for index in original_train if index in kept[variant]]
        removed = [index for index in original_train if index not in kept[variant]]
        labels_before = Counter(rows[i]["label"] for i in original_train)
        labels_after = Counter(rows[i]["label"] for i in keep)
        manifest = {
            "schema_version": "stage5_conflict_manifest_v1",
            "variant_id": variant,
            "created_utc": generated_utc,
            "commit": None,
            "source_path": config["source"]["path"],
            "source_sha256": source_hash,
            "split_path": config["split"]["path"],
            "split_id": split["id"],
            "split_sha256": split_hash,
            "row_manifest_path": config["row_manifest"]["path"],
            "row_manifest_sha256": row_hash,
            "grouping_version": config["grouping"]["version"],
            "normalization": config["grouping"]["normalization"],
            "seed": config["fixed_training_protocol"]["seed"],
            "fold": 1,
            "original_train_indices": original_train,
            "retained_train_indices": keep,
            "removed_train_indices": removed,
            "original_train_count": len(original_train),
            "retained_train_count": len(keep),
            "removed_train_count": len(removed),
            "removed_train_percent": round(100 * len(removed) / len(original_train), 6),
            "class_counts_before": {label: labels_before[label] for label in LABELS},
            "class_counts_after": {label: labels_after[label] for label in LABELS},
            "validation_indices": validation,
            "validation_indices_sha256": validation_hash,
            "holdout_indices_sha256": holdout_hash,
            "conflicting_groups": conflict_data,
            "normalization_uses_near_duplicates": False,
        }
        path = manifest_dir / filename
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest["manifest_sha256"] = digest_file(path)
        # Store the self hash in a separate sidecar so the manifest hash itself stays non-recursive.
        (path.with_suffix(".sha256")).write_text(manifest["manifest_sha256"] + "\n", encoding="ascii")
    return validate_all(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    summary = validate_all(args.root) if args.validate_only else create_manifests(args.root)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
