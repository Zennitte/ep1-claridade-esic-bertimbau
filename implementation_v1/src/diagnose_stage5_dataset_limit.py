"""Inference-only fold-1 diagnostics for Stage 5c.2; never accesses the holdout rows."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding

from audit_and_split import digest_file


LABELS = ["c1", "c234", "c5"]
ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "0e9219233664ac675fc47982bbc822acd3bb15d67fb7bfc26b67bec047e46818"


class TextDataset(Dataset):
    def __init__(self, encodings: dict, targets: list[int]):
        self.encodings = encodings
        self.targets = targets

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, index):
        return {key: values[index] for key, values in self.encodings.items()} | {"labels": self.targets[index]}


def classification(true_ids: list[int], pred_ids: list[int]) -> dict:
    cm = [[0 for _ in LABELS] for _ in LABELS]
    for true, pred in zip(true_ids, pred_ids):
        cm[true][pred] += 1
    per_class = {}
    total = len(true_ids)
    for i, label in enumerate(LABELS):
        tp = cm[i][i]
        support = sum(cm[i])
        predicted = sum(row[i] for row in cm)
        precision = tp / predicted if predicted else 0.0
        recall = tp / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[label] = {"support": support, "predicted_count": predicted,
                            "precision": precision, "recall": recall, "f1": f1}
    accuracy = sum(cm[i][i] for i in range(len(LABELS))) / total if total else 0.0
    macro_f1 = sum(per_class[label]["f1"] for label in LABELS) / len(LABELS)
    weighted_f1 = sum(per_class[label]["f1"] * per_class[label]["support"] for label in LABELS) / total
    return {"rows": total, "accuracy": accuracy, "macro_f1": macro_f1, "weighted_f1": weighted_f1,
            "confusion_matrix_rows_true_cols_pred": cm, "by_class": per_class}


def read_partition_rows(indices: list[int], split: dict) -> tuple[dict[int, str], dict[int, str]]:
    """Extract only requested data rows from the XLSX XML; discard all other rows."""
    source = ROOT / split["source"]
    if digest_file(source) != SOURCE_SHA256 or split["source_sha256"] != SOURCE_SHA256:
        raise ValueError("Source hash does not match the frozen training source")
    requested_indices = sorted(set(indices))
    if len(requested_indices) != len(indices):
        raise ValueError("Duplicate indices in requested fold partition")
    wanted_rows = {idx + 2: idx for idx in requested_indices}
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    cells, shared_refs, wanted_shared = {}, {}, set()
    with zipfile.ZipFile(source) as archive:
        names = set(archive.namelist())
        if "xl/worksheets/sheet1.xml" not in names:
            raise ValueError("Expected the single train worksheet at xl/worksheets/sheet1.xml")
        with archive.open("xl/worksheets/sheet1.xml") as stream:
            for _, row_elem in ET.iterparse(stream, events=("end",)):
                if row_elem.tag != f"{ns}row":
                    continue
                excel_row = int(row_elem.attrib["r"])
                if excel_row in wanted_rows:
                    idx = wanted_rows[excel_row]
                    for cell in row_elem.findall(f"{ns}c"):
                        coord = cell.attrib.get("r", "")
                        col = re.match(r"([A-Z]+)", coord).group(1)
                        if col not in {"A", "B"}:
                            continue
                        kind = cell.attrib.get("t")
                        if kind == "s":
                            ref = int(cell.findtext(f"{ns}v"))
                            shared_refs[(idx, col)] = ref
                            wanted_shared.add(ref)
                        elif kind == "inlineStr":
                            value = "".join(cell.find(f"{ns}is").itertext())
                            cells[(idx, col)] = value
                        else:
                            cells[(idx, col)] = cell.findtext(f"{ns}v")
                row_elem.clear()
        shared = {}
        if wanted_shared:
            if "xl/sharedStrings.xml" not in names:
                raise ValueError("Worksheet references shared strings but sharedStrings.xml is missing")
            with archive.open("xl/sharedStrings.xml") as stream:
                shared_index = -1
                for _, si in ET.iterparse(stream, events=("end",)):
                    if si.tag != f"{ns}si":
                        continue
                    shared_index += 1
                    if shared_index in wanted_shared:
                        shared[shared_index] = "".join(si.itertext())
                    si.clear()
    for key, ref in shared_refs.items():
        cells[key] = shared[ref]
    texts = {idx: cells[(idx, "A")] for idx in requested_indices}
    labels = {idx: cells[(idx, "B")] for idx in requested_indices}
    for idx, value in list(texts.items()):
        texts[idx] = value if isinstance(value, str) else str(value)
    return texts, labels


def load_group_ids(indices: set[int]) -> dict[int, str]:
    result = {}
    with (ROOT / "data/row_manifest.csv").open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            idx = int(row["row_index"])
            if idx in indices:
                result[idx] = row["group_sha256"]
    if set(result) != indices:
        raise ValueError("Could not match every diagnostic row to row_manifest.csv")
    return result


def infer_partition(model, tokenizer, device, indices: list[int], texts: dict[int, str], labels: dict[int, str],
                    groups: dict[int, str], batch_size: int) -> tuple[dict, list[dict]]:
    ordered_texts = [texts[i] for i in indices]
    enc = tokenizer(ordered_texts, truncation=True, max_length=512, padding=False)
    full_lengths = [len(ids) for ids in tokenizer(ordered_texts, add_special_tokens=True,
                                                  truncation=False)["input_ids"]]
    dataset = TextDataset(enc, [LABELS.index(labels[i]) for i in indices])
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0,
                        collate_fn=DataCollatorWithPadding(tokenizer, return_tensors="pt"))
    rows, true_ids, pred_ids, losses = [], [], [], []
    model.eval()
    with torch.inference_mode():
        for batch_no, batch in enumerate(loader, 1):
            batch = {key: value.to(device) for key, value in batch.items()}
            targets = batch.pop("labels")
            logits = model(**batch).logits.float()
            probs = torch.softmax(logits, dim=-1).cpu().numpy()
            target_list = targets.cpu().tolist()
            predicted = logits.argmax(dim=-1).cpu().tolist()
            losses.extend(torch.nn.functional.cross_entropy(logits, targets, reduction="none").cpu().tolist())
            true_ids.extend(target_list)
            pred_ids.extend(predicted)
            batch_indices = indices[(batch_no - 1) * batch_size: batch_no * batch_size]
            start = (batch_no - 1) * batch_size
            for offset, (idx, true_id, pred_id, p) in enumerate(zip(batch_indices, target_list, predicted, probs)):
                order = np.sort(p)
                entropy = -sum(float(v) * math.log(float(v)) for v in p if v > 0)
                rows.append({
                    "row_index": idx, "excel_row": idx + 2, "group_sha256": groups[idx],
                    "text": texts[idx], "true": LABELS[true_id], "pred": LABELS[pred_id],
                    "probabilities": {label: float(p[j]) for j, label in enumerate(LABELS)},
                    "confidence": float(order[-1]), "second_probability": float(order[-2]),
                    "margin_top1_top2": float(order[-1] - order[-2]), "entropy_nats": float(entropy),
                    "truncated_at_512": full_lengths[start + offset] > 512,
                })
            if batch_no % 100 == 0 or batch_no == len(loader):
                print(f"partition rows={len(rows)}/{len(indices)}", flush=True)
    summary = classification(true_ids, pred_ids)
    summary["cross_entropy_loss"] = float(np.mean(losses))
    summary["mean_encoded_tokens"] = float(np.mean([len(item) for item in enc["input_ids"]]))
    summary["truncated_rows_512"] = sum(row["truncated_at_512"] for row in rows)
    return summary, rows


def select_qualitative_samples(prediction_path: Path, output_path: Path) -> None:
    rows = [json.loads(line) for line in prediction_path.read_text(encoding="utf-8").split("\n") if line]
    confidences = np.asarray([row["confidence"] for row in rows])
    low, high = np.quantile(confidences, [0.25, 0.75])
    by_index = {}

    def add(candidates: list[dict], reason: str, count: int) -> None:
        for row in candidates[:count]:
            entry = by_index.setdefault(row["row_index"], dict(row, selection_reasons=[]))
            if reason not in entry["selection_reasons"]:
                entry["selection_reasons"].append(reason)

    groups = [
        ("correct_high_confidence", [r for r in rows if r["true"] == r["pred"] and r["confidence"] >= high],
         lambda r: -r["confidence"]),
        ("correct_low_confidence", [r for r in rows if r["true"] == r["pred"] and r["confidence"] <= low],
         lambda r: r["confidence"]),
        ("error_high_confidence", [r for r in rows if r["true"] != r["pred"] and r["confidence"] >= high],
         lambda r: -r["confidence"]),
        ("error_low_confidence", [r for r in rows if r["true"] != r["pred"] and r["confidence"] <= low],
         lambda r: r["confidence"]),
    ]
    for reason, candidates, key in groups:
        add(sorted(candidates, key=lambda r: (key(r), r["row_index"])), reason, 6)
    directions = [("c1", "c234"), ("c1", "c5"), ("c234", "c1"), ("c234", "c5"),
                  ("c5", "c1"), ("c5", "c234")]
    for true, pred in directions:
        candidates = [r for r in rows if r["true"] == true and r["pred"] == pred]
        candidates.sort(key=lambda r: (r["confidence"], r["row_index"]))
        reason = f"error_{true}_to_{pred}"
        if candidates:
            half = 4
            chosen = candidates[:half] + candidates[-half:]
            add(chosen, reason, len(chosen))
    selected = sorted(by_index.values(), key=lambda r: (r["true"], r["pred"], r["row_index"]))
    output_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in selected) + "\n", encoding="utf-8")
    appendix = ROOT / "reports/etapa5_dataset_limit_diagnosis_examples.md"
    lines = ["# Apêndice — amostra qualitativa da 5c.2", "",
             f"Amostra determinística de {len(selected)} linhas da validação do fold 1. Os rótulos foram preservados. "
             "A seleção cobre acertos/erros de confiança alta/baixa e os seis sentidos de confusão entre classes. "
             "Confiança alta/baixa foi definida pelos quartis 75/25 da confiança top-1 na validação.", ""]
    for n, row in enumerate(selected, 1):
        probabilities = ", ".join(f"{label}={row['probabilities'][label]:.4f}" for label in LABELS)
        model_text = row.get("model_input_text", row["text"])
        quoted_text = "\n".join("> " + part for part in model_text.replace("```", "''' ").splitlines())
        lines.extend([
            f"## Exemplo {n} — linha Excel {row['excel_row']}", "",
            f"- Seleção: {', '.join(row['selection_reasons'])}",
            f"- Verdadeiro → predito: `{row['true']}` → `{row['pred']}`",
            f"- Probabilidades: {probabilities}",
            f"- Confiança top-1 / margem top-1−top-2 / entropia: {row['confidence']:.4f} / {row['margin_top1_top2']:.4f} / {row['entropy_nats']:.4f} nats",
            f"- Grupo normalizado (SHA-256): `{row['group_sha256']}`",
            f"- Entrada truncada em 512 tokens: `{row['truncated_at_512']}`", "",
            "Texto efetivamente usado pelo modelo (tokens decodificados após truncamento):", "", quoted_text or "> [texto vazio]", "",
        ])
    appendix.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"samples": len(selected), "low_confidence_q25": float(low),
                      "high_confidence_q75": float(high), "transition_counts": {
                          f"{a}->{b}": sum(r["true"] == a and r["pred"] == b for r in rows) for a, b in directions
                      }, "output": str(output_path.relative_to(ROOT)),
                      "appendix": str(appendix.relative_to(ROOT))}, ensure_ascii=False, indent=2))


def analyze_tfidf_similarity(split: dict, fold: dict, output_path: Path) -> None:
    train_indices, valid_indices = list(fold["train"]), list(fold["validation"])
    all_indices = train_indices + valid_indices
    texts, labels = read_partition_rows(all_indices, split)
    vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=3, max_features=100000,
                                 sublinear_tf=True, lowercase=True, norm="l2")
    train_matrix = vectorizer.fit_transform([texts[i] for i in train_indices])
    valid_matrix = vectorizer.transform([texts[i] for i in valid_indices])
    train_label_ids = np.asarray([LABELS.index(labels[i]) for i in train_indices])
    valid_label_ids = np.asarray([LABELS.index(labels[i]) for i in valid_indices])
    row_positions = np.flatnonzero(valid_label_ids == LABELS.index("c234"))
    max_sims, top5_sims = {}, {}
    for class_id, candidate_label in enumerate(LABELS):
        class_matrix = train_matrix[train_label_ids == class_id]
        maxima, top5_means = [], []
        for start in range(0, len(row_positions), 64):
            query = valid_matrix[row_positions[start:start + 64]]
            similarities = (query @ class_matrix.T).tocsr()
            for row_no in range(similarities.shape[0]):
                values = similarities.data[similarities.indptr[row_no]:similarities.indptr[row_no + 1]]
                if len(values):
                    ordered = np.sort(values)[::-1]
                    maxima.append(float(ordered[0]))
                    top5_means.append(float(np.mean(ordered[:5])))
                else:
                    maxima.append(0.0)
                    top5_means.append(0.0)
        max_sims[candidate_label] = maxima
        top5_sims[candidate_label] = top5_means
    closest_counts = {label: 0 for label in LABELS}
    for i in range(len(row_positions)):
        nearest = max(LABELS, key=lambda label: max_sims[label][i])
        closest_counts[nearest] += 1
    summary = {"true_class": "c234", "n": int(len(row_positions)),
               "by_nearest_train_class": {}, "nearest_neighbor_label_counts": closest_counts}
    for candidate_label in LABELS:
        summary["by_nearest_train_class"][candidate_label] = {
            "mean_max_cosine": float(np.mean(max_sims[candidate_label])),
            "median_max_cosine": float(np.median(max_sims[candidate_label])),
            "mean_top5_cosine": float(np.mean(top5_sims[candidate_label])),
        }
    output = {
        "method": "fold-1 train-only TF-IDF word uni/bigrams; per-validation-row maximum and top-5 cosine to each training class",
        "vectorizer": {"ngram_range": [1, 2], "min_df": 3, "max_features": 100000,
                       "sublinear_tf": True, "lowercase": True, "norm": "l2"},
        "train_rows": len(train_indices), "validation_rows": len(valid_indices),
        "holdout_evaluated": False, "intermediate_class_diagnostics": summary,
        "interpretation_limit": "Similarity is lexical, not semantic; it is exploratory and does not estimate human labelability.",
    }
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--select-samples", action="store_true")
    parser.add_argument("--enrich-inputs", action="store_true")
    parser.add_argument("--text-similarity", action="store_true")
    args = parser.parse_args()
    output_dir = ROOT / "runs/etapa5/diagnose_fold1_dataset_limit_20260925"
    if args.enrich_inputs:
        prediction_path = output_dir / "validation_predictions.jsonl"
        rows = [json.loads(line) for line in prediction_path.read_text(encoding="utf-8").split("\n") if line]
        run_metrics = json.loads((output_dir / "metrics.json").read_text(encoding="utf-8"))
        tokenizer = AutoTokenizer.from_pretrained(ROOT / run_metrics["checkpoint"], local_files_only=True)
        for start in range(0, len(rows), 128):
            chunk = rows[start:start + 128]
            enc = tokenizer([row["text"] for row in chunk], truncation=True, max_length=512, padding=False)
            for row, input_ids in zip(chunk, enc["input_ids"]):
                row["model_input_text"] = tokenizer.decode(input_ids, skip_special_tokens=True,
                                                          clean_up_tokenization_spaces=False)
        prediction_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
                                   encoding="utf-8")
        print(f"Adicionado o texto decodificado de entrada para {len(rows)} exemplos de validação.")
        return
    if args.select_samples:
        select_qualitative_samples(output_dir / "validation_predictions.jsonl", output_dir / "qualitative_samples.jsonl")
        return
    split = json.loads((ROOT / "data/splits_grouped_v1.json").read_text(encoding="utf-8"))
    fold = next(f for f in split["folds"] if f["fold"] == 1)
    if args.text_similarity:
        analyze_tfidf_similarity(split, fold, output_dir / "tfidf_similarity.json")
        return
    train_indices, valid_indices = list(fold["train"]), list(fold["validation"])
    # Deliberately never read split["holdout"] or materialize any row outside fold 1.
    assert not set(train_indices).intersection(valid_indices)
    config = json.loads((ROOT / "configs/bert_stage5_conflict_ablation.json").read_text(encoding="utf-8"))
    record = config["variant_run_records"]["A_original"]
    metric_path = ROOT / record["metrics_path"]
    metrics = json.loads(metric_path.read_text(encoding="utf-8"))
    if metrics["source_sha256"] != SOURCE_SHA256 or metrics["config"]["fold"] != 1 or not metrics["full_fold"]:
        raise ValueError("Selected checkpoint metrics are not the expected full fold-1 run")
    if metrics["candidate"]["id"] != "start512_lr2e5" or metrics["best_optimizer_step"] != 2688:
        raise ValueError("Selected checkpoint is not the 5c reference checkpoint")
    all_indices = train_indices + valid_indices
    texts, labels = read_partition_rows(all_indices, split)
    if set(labels.values()) - set(LABELS):
        raise ValueError("Unexpected target labels in fold-1 development data")
    groups = load_group_ids(set(all_indices))
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA/ROCm device requested but unavailable")
    device = torch.device("cuda:0" if args.device == "cuda" or (args.device == "auto" and torch.cuda.is_available()) else "cpu")
    checkpoint = ROOT / metrics["checkpoint"]
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint, local_files_only=True).to(device)
    print(f"device={device}; checkpoint={checkpoint.relative_to(ROOT)}; no training", flush=True)
    train_summary, _ = infer_partition(model, tokenizer, device, train_indices, texts, labels, groups, args.batch_size)
    valid_summary, valid_rows = infer_partition(model, tokenizer, device, valid_indices, texts, labels, groups, args.batch_size)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(json.dumps({
        "source_sha256": SOURCE_SHA256,
        "split_id": split["id"],
        "fold": 1,
        "reference_run": record["run_id"],
        "checkpoint": str(checkpoint.relative_to(ROOT)),
        "device": str(device),
        "max_length": 512,
        "holdout_evaluated": False,
        "train": train_summary,
        "validation": valid_summary,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "validation_predictions.jsonl").open("w", encoding="utf-8") as f:
        for row in valid_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"train": train_summary, "validation": valid_summary,
                      "metrics_path": str((output_dir / "metrics.json").relative_to(ROOT)),
                      "validation_predictions_path": str((output_dir / "validation_predictions.jsonl").relative_to(ROOT))},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
