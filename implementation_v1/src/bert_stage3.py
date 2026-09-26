"""Benchmark e execução curta de fine-tuning do BERTimbau Base."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import openpyxl
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding

from audit_and_split import digest_file
from experiment_metrics import classification_metrics
from plot_curves import plot_series_svg


class EncodedDataset(Dataset):
    def __init__(self, encoded: dict, labels: list[int]):
        self.encoded = encoded
        self.labels = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, index: int) -> dict:
        return {key: values[index] for key, values in self.encoded.items()} | {"labels": self.labels[index]}


def read_dataset(root: Path, split: dict) -> tuple[list[str], list[str]]:
    source = root / split["source"]
    if digest_file(source) != split["source_sha256"]:
        raise ValueError("train.xlsx não corresponde ao hash da divisão congelada")
    workbook = openpyxl.load_workbook(source, read_only=True, data_only=True)
    rows = list(workbook["train"].iter_rows(min_row=2, max_col=2, values_only=True))
    workbook.close()
    text = [value if isinstance(value, str) else str(value) for value, _ in rows]
    labels = [label for _, label in rows]
    return text, labels


def choose_rows(indices: list[int], count: int, seed: int) -> list[int]:
    return sorted(random.Random(seed).sample(indices, min(count, len(indices))))


def make_loader(
    tokenizer, texts: list[str], labels: list[str], indices: list[int], label2id: dict,
    max_length: int, batch_size: int, shuffle: bool, seed: int,
) -> DataLoader:
    encoded = tokenizer(
        [texts[index] for index in indices], truncation=True, max_length=max_length,
        padding=False, add_special_tokens=True,
    )
    dataset = EncodedDataset(encoded, [label2id[labels[index]] for index in indices])
    generator = torch.Generator().manual_seed(seed)
    return DataLoader(
        dataset, batch_size=batch_size, shuffle=shuffle, generator=generator,
        collate_fn=DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt"), num_workers=0,
    )


def evaluate(model, loader, device, class_names: list[str]) -> dict:
    model.eval()
    all_true, all_pred = [], []
    losses = []
    started = time.perf_counter()
    with torch.inference_mode():
        for batch in loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            output = model(**batch)
            losses.append(float(output.loss.item()) * len(batch["labels"]))
            all_true.extend(batch["labels"].tolist())
            all_pred.extend(output.logits.argmax(dim=-1).tolist())
    torch.cuda.synchronize(device)
    true_names = [class_names[index] for index in all_true]
    pred_names = [class_names[index] for index in all_pred]
    return {
        "loss": sum(losses) / len(all_true),
        "metrics": classification_metrics(true_names, pred_names, class_names),
        "rows": len(all_true),
        "seconds": round(time.perf_counter() - started, 3),
    }


def load_model(config: dict):
    names = config["labels"]
    label2id = {name: index for index, name in enumerate(names)}
    id2label = {index: name for name, index in label2id.items()}
    return AutoModelForSequenceClassification.from_pretrained(
        config["model_id"], num_labels=len(names), label2id=label2id, id2label=id2label,
        local_files_only=True,
    )


def run(root: Path, mode: str, run_id: str) -> dict:
    started = time.perf_counter()
    config = json.loads((root / "configs" / "bert_stage3.json").read_text(encoding="utf-8"))
    split_path = root / "data" / "splits_grouped_v1.json"
    split = json.loads(split_path.read_text(encoding="utf-8"))
    if split["id"] != config["split_id"]:
        raise ValueError("Configuração e divisão não correspondem")
    if not torch.cuda.is_available():
        raise RuntimeError("GPU ROCm indisponível")
    device = torch.device("cuda:0")
    torch.manual_seed(config["seed"])
    np.random.seed(config["seed"])
    random.seed(config["seed"])
    device_properties = torch.cuda.get_device_properties(device)
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats(device)
    run_dir = root / "runs" / "etapa3" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    fold = next(item for item in split["folds"] if item["fold"] == config["fold"])
    assert not set(fold["train"]).intersection(split["holdout"])
    assert not set(fold["validation"]).intersection(split["holdout"])
    texts, labels = read_dataset(root, split)
    tokenizer = AutoTokenizer.from_pretrained(config["model_id"], local_files_only=True)
    label2id = {name: index for index, name in enumerate(config["labels"])}
    train_count = 96 if mode == "benchmark" else config["short_train_rows"]
    valid_count = 0 if mode == "benchmark" else config["short_validation_rows"]
    train_rows = choose_rows(fold["train"], train_count, config["seed"])
    valid_rows = choose_rows(fold["validation"], valid_count, config["seed"] + 1) if valid_count else []
    train_loader = make_loader(
        tokenizer, texts, labels, train_rows, label2id, config["max_length"],
        config["micro_batch_size"], True, config["seed"],
    )
    valid_loader = make_loader(
        tokenizer, texts, labels, valid_rows, label2id, config["max_length"],
        config["micro_batch_size"] * 2, False, config["seed"],
    ) if valid_rows else None
    model = load_model(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config["learning_rate"], weight_decay=config["weight_decay"])
    result = {
        "run_id": run_id,
        "mode": mode,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": split["source_sha256"],
        "split_id": split["id"],
        "split_sha256": digest_file(split_path),
        "config": config,
        "train_rows": len(train_rows),
        "validation_rows": len(valid_rows),
        "holdout_evaluated": False,
        "versions": {name: version(name) for name in ("torch", "transformers", "tokenizers", "openpyxl")},
        "gpu": {"name": device_properties.name, "total_memory_bytes": device_properties.total_memory},
        "history": [],
    }
    max_micro = config["benchmark_micro_batches"] if mode == "benchmark" else config["short_optimizer_steps"] * config["gradient_accumulation_steps"]
    accum = config["gradient_accumulation_steps"]
    model.train()
    optimizer.zero_grad(set_to_none=True)
    micro_steps = optimizer_steps = 0
    recent_loss = recent_correct = recent_rows = 0
    recent_micro_seconds = []
    best_score = (-1.0, -1.0)
    best_step = None
    stale_evaluations = 0
    checkpoint = root / "models" / "bert_stage3" / run_id / "best"
    train_started = time.perf_counter()
    while micro_steps < max_micro:
        for batch in train_loader:
            if micro_steps >= max_micro:
                break
            batch = {key: value.to(device) for key, value in batch.items()}
            model.train()
            step_started = time.perf_counter()
            output = model(**batch)
            loss = output.loss / accum
            loss.backward()
            micro_steps += 1
            recent_loss += float(output.loss.item()) * len(batch["labels"])
            recent_correct += int((output.logits.argmax(dim=-1) == batch["labels"]).sum().item())
            recent_rows += len(batch["labels"])
            if micro_steps % accum == 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                optimizer.zero_grad(set_to_none=True)
                optimizer_steps += 1
            torch.cuda.synchronize(device)
            recent_micro_seconds.append(time.perf_counter() - step_started)
            if mode == "benchmark" or micro_steps % (accum * config["eval_every_optimizer_steps"]) != 0:
                continue
            train_metrics = {
                "loss": recent_loss / recent_rows,
                "accuracy": recent_correct / recent_rows,
                "rows_seen_since_last_eval": recent_rows,
            }
            validation = evaluate(model, valid_loader, device, config["labels"])
            point = {"optimizer_step": optimizer_steps, "train": train_metrics, "validation": validation}
            result["history"].append(point)
            print(
                f"step={optimizer_steps} train_loss={train_metrics['loss']:.4f} "
                f"train_acc={train_metrics['accuracy']:.4f} "
                f"valid_loss={validation['loss']:.4f} "
                f"valid_acc={validation['metrics']['accuracy']:.4f}", flush=True,
            )
            score = (validation["metrics"]["accuracy"], validation["metrics"]["macro_f1"])
            if score > best_score:
                best_score = score
                best_step = optimizer_steps
                checkpoint.mkdir(parents=True, exist_ok=True)
                model.save_pretrained(checkpoint, safe_serialization=True)
                tokenizer.save_pretrained(checkpoint)
                stale_evaluations = 0
            else:
                stale_evaluations += 1
            (run_dir / "metrics_partial.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            recent_loss = recent_correct = recent_rows = 0
            if stale_evaluations >= config["early_stopping_patience_evaluations"]:
                break
        if mode == "benchmark" or stale_evaluations >= config["early_stopping_patience_evaluations"]:
            break
    torch.cuda.synchronize(device)
    result["training_wall_seconds"] = round(time.perf_counter() - train_started, 3)
    result["micro_batches"] = micro_steps
    result["optimizer_steps"] = optimizer_steps
    result["mean_micro_batch_seconds"] = round(float(np.mean(recent_micro_seconds)), 4)
    result["median_micro_batch_seconds"] = round(float(np.median(recent_micro_seconds)), 4)
    result["gpu"]["peak_allocated_bytes"] = torch.cuda.max_memory_allocated(device)
    result["gpu"]["peak_reserved_bytes"] = torch.cuda.max_memory_reserved(device)
    result["examples_per_second_training"] = round(micro_steps * config["micro_batch_size"] / result["training_wall_seconds"], 3)
    result["estimated_full_fold_one_epoch_seconds"] = round(
        math.ceil(len(fold["train"]) / config["micro_batch_size"]) * result["mean_micro_batch_seconds"], 1
    )
    if mode == "short":
        if best_step is None:
            raise RuntimeError("Nenhum checkpoint de validação foi salvo")
        del model, optimizer
        torch.cuda.empty_cache()
        loaded = AutoModelForSequenceClassification.from_pretrained(checkpoint).to(device)
        loaded_tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
        sample = loaded_tokenizer(
            [texts[index] for index in valid_rows[:5]], truncation=True,
            max_length=config["max_length"], padding=True, return_tensors="pt",
        ).to(device)
        loaded.eval()
        with torch.inference_mode():
            logits = loaded(**sample).logits
        torch.cuda.synchronize(device)
        result["checkpoint"] = str(checkpoint.relative_to(root))
        result["best_optimizer_step"] = best_step
        result["checkpoint_reload"] = {
            "five_logits_shape": list(logits.shape),
            "predicted_labels": [config["labels"][index] for index in logits.argmax(dim=-1).tolist()],
            "all_finite": bool(torch.isfinite(logits).all().item()),
        }
        if result["checkpoint_reload"]["five_logits_shape"] != [5, 3] or not result["checkpoint_reload"]["all_finite"]:
            raise RuntimeError("Falha na verificação do checkpoint recarregado")
        result["early_stopped"] = stale_evaluations >= config["early_stopping_patience_evaluations"]
    result["total_wall_seconds"] = round(time.perf_counter() - started, 3)
    (run_dir / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if result["history"]:
        for field, spec in (
            ("accuracy", ("Acurácia de treino e validação", "Acurácia")),
            ("loss", ("Loss de treino e validação", "Loss")),
        ):
            curve = {
                "title": spec[0], "x_label": "Passo do otimizador", "y_label": spec[1],
                "series": [
                    {"label": "Treino", "points": [[p["optimizer_step"], p["train"][field]] for p in result["history"]]},
                    {"label": "Validação", "points": [[p["optimizer_step"], (p["validation"]["metrics"]["accuracy"] if field == "accuracy" else p["validation"]["loss"])] for p in result["history"]]},
                ],
            }
            plot_series_svg(curve, root / "reports" / f"etapa3_{field}_curve.svg")
    print(json.dumps({"run_id": run_id, "mode": mode, "steps": optimizer_steps, "wall_seconds": result["total_wall_seconds"], "gpu": result["gpu"], "best_step": best_step}, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("benchmark", "short"))
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    run_id = args.run_id or f"bert_stage3_{args.mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run(Path(__file__).resolve().parents[1], args.mode, run_id)


if __name__ == "__main__":
    main()
