"""Triagem controlada de representações e taxa de aprendizado do BERTimbau."""

from __future__ import annotations

import argparse
import json
import random
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, DataCollatorWithPadding

from audit_and_split import digest_file
from bert_stage3 import EncodedDataset, evaluate, load_model, read_dataset
from plot_curves import plot_series_svg


def encode(tokenizer, texts: list[str], representation: str, max_length: int) -> tuple[dict, dict]:
    if representation == "start":
        encoded = tokenizer(texts, truncation=True, max_length=max_length, padding=False)
        full_lengths = [len(ids) for ids in tokenizer(texts, add_special_tokens=True, truncation=False)["input_ids"]]
    elif representation == "head_tail":
        bodies = tokenizer(texts, add_special_tokens=False, truncation=False)["input_ids"]
        capacity = max_length - tokenizer.num_special_tokens_to_add(pair=False)
        first = capacity // 2
        last = capacity - first
        ids_list = []
        for body in bodies:
            chosen = body if len(body) <= capacity else body[:first] + body[-last:]
            ids_list.append(tokenizer.build_inputs_with_special_tokens(chosen))
        encoded = {
            "input_ids": ids_list,
            "attention_mask": [[1] * len(ids) for ids in ids_list],
            "token_type_ids": [[0] * len(ids) for ids in ids_list],
        }
        full_lengths = [len(body) + tokenizer.num_special_tokens_to_add(pair=False) for body in bodies]
    else:
        raise ValueError(f"Representação desconhecida: {representation}")
    return encoded, {
        "rows": len(texts),
        "truncated_rows": sum(length > max_length for length in full_lengths),
        "mean_encoded_tokens": round(float(np.mean([len(ids) for ids in encoded["input_ids"]])), 2),
        "max_encoded_tokens": max(len(ids) for ids in encoded["input_ids"]),
    }


def loader(tokenizer, encoded, labels, indices, label2id, batch_size, shuffle, seed):
    dataset = EncodedDataset(encoded, [label2id[labels[index]] for index in indices])
    return DataLoader(
        dataset, batch_size=batch_size, shuffle=shuffle,
        generator=torch.Generator().manual_seed(seed), num_workers=0,
        collate_fn=DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt"),
    )


def run(
    root: Path, candidate_id: str, run_id: str, *, fold_override: int | None = None,
    full_fold: bool = False, max_optimizer_steps: int | None = None,
    eval_every_optimizer_steps: int | None = None, run_stage: int = 4,
    train_indices_manifest: Path | None = None,
) -> dict:
    started = time.perf_counter()
    config_path = root / "configs" / "bert_stage4.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if fold_override is not None:
        config["fold"] = fold_override
    if eval_every_optimizer_steps is not None:
        config["eval_every_optimizer_steps"] = eval_every_optimizer_steps
    candidate = next((item for item in config["candidates"] if item["id"] == candidate_id), None)
    if candidate is None:
        raise ValueError(f"Candidato desconhecido: {candidate_id}")
    split_path = root / "data" / "splits_grouped_v1.json"
    split = json.loads(split_path.read_text(encoding="utf-8"))
    if config["split_id"] != split["id"]:
        raise ValueError("Divisão não corresponde à configuração")
    fold = next(item for item in split["folds"] if item["fold"] == config["fold"])
    subset_path = root / "data" / "stage4_subset.json"
    if full_fold:
        subset = None
        train_indices = list(fold["train"])
        valid_indices = list(fold["validation"])
        subset_id = f"full_fold_{config['fold']}"
        subset_sha256 = None
    else:
        subset = json.loads(subset_path.read_text(encoding="utf-8"))
        if subset["split_sha256"] != digest_file(split_path):
            raise ValueError("Divisão ou amostra não corresponde ao protocolo")
        if subset["source_sha256"] != split["source_sha256"]:
            raise ValueError("Fonte da amostra diferente da divisão")
        train_indices = subset["train"]
        valid_indices = subset["validation"]
        subset_id = subset["id"]
        subset_sha256 = digest_file(subset_path)
    manifest_info = None
    if train_indices_manifest is not None:
        if not full_fold:
            raise ValueError("Manifesto de treino só pode ser usado junto de --full-fold")
        manifest_path = train_indices_manifest if train_indices_manifest.is_absolute() else root / train_indices_manifest
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["fold"] != config["fold"] or manifest["split_id"] != split["id"]:
            raise ValueError("Manifesto de treino pertence a outra divisão ou fold")
        if manifest["source_sha256"] != split["source_sha256"]:
            raise ValueError("Manifesto de treino pertence a outra planilha de origem")
        if manifest["split_sha256"] != digest_file(split_path):
            raise ValueError("Hash da divisão no manifesto diverge")
        row_manifest_path = root / "data/row_manifest.csv"
        if manifest["row_manifest_sha256"] != digest_file(row_manifest_path):
            raise ValueError("Hash do manifesto de linhas diverge")
        if manifest["original_train_indices"] != list(fold["train"]):
            raise ValueError("Manifesto não preserva os índices originais de treino")
        if manifest["validation_indices"] != valid_indices:
            raise ValueError("Manifesto tenta alterar a validação congelada")
        selected_indices = manifest["retained_train_indices"]
        if len(selected_indices) != len(set(selected_indices)) or not set(selected_indices).issubset(fold["train"]):
            raise ValueError("Manifesto tem índices duplicados ou fora do treino original")
        train_indices = list(selected_indices)
        subset_id = f"conflict_{manifest['variant_id']}"
        subset_sha256 = digest_file(manifest_path)
        manifest_info = {
            "path": str(manifest_path.relative_to(root)),
            "sha256": subset_sha256,
            "variant_id": manifest["variant_id"],
            "retained_train_count": len(train_indices),
            "removed_train_count": len(manifest["removed_train_indices"]),
            "removed_train_percent": manifest["removed_train_percent"],
        }
    if not torch.cuda.is_available():
        raise RuntimeError("GPU ROCm indisponível")
    device = torch.device("cuda:0")
    props = torch.cuda.get_device_properties(device)
    torch.manual_seed(config["seed"])
    np.random.seed(config["seed"])
    random.seed(config["seed"])
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats(device)
    run_dir = root / "runs" / f"etapa{run_stage}" / run_id
    checkpoint = root / "models" / f"bert_stage{run_stage}" / run_id / "best"
    run_dir.mkdir(parents=True, exist_ok=False)
    effective_config = {**config, "candidate": candidate}
    (run_dir / "config.json").write_text(json.dumps(effective_config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text, labels = read_dataset(root, split)
    tokenizer = AutoTokenizer.from_pretrained(config["model_id"], local_files_only=True)
    assert set(train_indices).issubset(fold["train"])
    assert set(valid_indices).issubset(fold["validation"])
    assert not set(train_indices).intersection(valid_indices)
    label2id = {label: index for index, label in enumerate(config["labels"])}
    train_encoded, train_token_stats = encode(
        tokenizer, [text[index] for index in train_indices], candidate["representation"], candidate["max_length"]
    )
    valid_encoded, valid_token_stats = encode(
        tokenizer, [text[index] for index in valid_indices], candidate["representation"], candidate["max_length"]
    )
    train_loader = loader(
        tokenizer, train_encoded, labels, train_indices, label2id,
        config["micro_batch_size"], True, config["seed"],
    )
    valid_loader = loader(
        tokenizer, valid_encoded, labels, valid_indices, label2id,
        config["micro_batch_size"] * 2, False, config["seed"],
    )
    model = load_model(config).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=candidate["learning_rate"], weight_decay=config["weight_decay"]
    )
    accumulation = config["gradient_accumulation_steps"]
    optimizer_steps_per_epoch = len(train_loader) // accumulation
    max_steps = optimizer_steps_per_epoch * config["max_epochs"]
    if max_optimizer_steps is not None:
        if max_optimizer_steps < 1:
            raise ValueError("max_optimizer_steps precisa ser positivo")
        max_steps = min(max_steps, max_optimizer_steps)
    result = {
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "candidate": candidate,
        "config": config,
        "source_sha256": split["source_sha256"],
        "split_id": split["id"],
        "split_sha256": digest_file(split_path),
        "subset_id": subset_id,
        "subset_sha256": subset_sha256,
        "train_indices_manifest": manifest_info,
        "full_fold": full_fold,
        "train_rows": len(train_indices),
        "validation_rows": len(valid_indices),
        "train_token_stats": train_token_stats,
        "validation_token_stats": valid_token_stats,
        "holdout_evaluated": False,
        "versions": {name: version(name) for name in ("torch", "transformers", "tokenizers", "openpyxl")},
        "gpu": {"name": props.name, "total_memory_bytes": props.total_memory},
        "history": [],
    }
    model.train()
    optimizer.zero_grad(set_to_none=True)
    best_score = (-1.0, -1.0)
    best_step = None
    stale = 0
    total_micro = total_steps = 0
    recent_rows = recent_correct = 0
    recent_loss = train_micro_seconds = eval_seconds = save_seconds = 0.0
    stop = False
    limit_reached = False
    effective_micro_batches_per_epoch = optimizer_steps_per_epoch * accumulation
    result["effective_micro_batches_per_epoch"] = effective_micro_batches_per_epoch
    result["dropped_train_rows_per_epoch"] = max(
        0, len(train_indices) - min(effective_micro_batches_per_epoch * config["micro_batch_size"], len(train_indices))
    )
    try:
        for epoch in range(1, config["max_epochs"] + 1):
            for batch_index, batch in enumerate(train_loader):
                # Do not carry a partial accumulation group into the next epoch.
                if batch_index >= effective_micro_batches_per_epoch:
                    break
                batch = {key: value.to(device) for key, value in batch.items()}
                model.train()
                step_started = time.perf_counter()
                output = model(**batch)
                (output.loss / accumulation).backward()
                total_micro += 1
                recent_rows += len(batch["labels"])
                recent_loss += float(output.loss.item()) * len(batch["labels"])
                recent_correct += int((output.logits.argmax(dim=-1) == batch["labels"]).sum().item())
                optimizer_step_completed = (batch_index + 1) % accumulation == 0
                if optimizer_step_completed:
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    optimizer.step()
                    optimizer.zero_grad(set_to_none=True)
                    total_steps += 1
                torch.cuda.synchronize(device)
                train_micro_seconds += time.perf_counter() - step_started
                scheduled_eval = optimizer_step_completed and total_steps % config["eval_every_optimizer_steps"] == 0
                epoch_end_eval = batch_index + 1 == effective_micro_batches_per_epoch
                final_eval = max_optimizer_steps is not None and total_steps == max_steps
                if total_steps == 0 or (not scheduled_eval and not epoch_end_eval and not final_eval):
                    continue
                train_metrics = {
                    "loss": recent_loss / recent_rows,
                    "accuracy": recent_correct / recent_rows,
                    "rows_seen_since_last_eval": recent_rows,
                }
                validation = evaluate(model, valid_loader, device, config["labels"])
                eval_seconds += validation["seconds"]
                point = {
                    "epoch": epoch,
                    "optimizer_step": total_steps,
                    "train": train_metrics,
                    "validation": validation,
                }
                result["history"].append(point)
                score = (validation["metrics"]["accuracy"], validation["metrics"]["macro_f1"])
                if score > best_score:
                    best_score = score
                    best_step = total_steps
                    checkpoint.mkdir(parents=True, exist_ok=True)
                    save_started = time.perf_counter()
                    model.save_pretrained(checkpoint, safe_serialization=True)
                    tokenizer.save_pretrained(checkpoint)
                    save_seconds += time.perf_counter() - save_started
                    stale = 0
                elif total_steps >= config["early_stopping_min_steps"]:
                    stale += 1
                result["best_optimizer_step"] = best_step
                result["best_validation_accuracy"] = best_score[0]
                (run_dir / "metrics_partial.json").write_text(
                    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
                print(
                    f"{candidate_id} step={total_steps}/{max_steps} epoch={epoch} "
                    f"train_loss={train_metrics['loss']:.4f} train_acc={train_metrics['accuracy']:.4f} "
                    f"valid_loss={validation['loss']:.4f} valid_acc={score[0]:.4f} "
                    f"valid_macro_f1={score[1]:.4f}", flush=True,
                )
                recent_rows = recent_correct = 0
                recent_loss = 0.0
                if total_steps >= config["early_stopping_min_steps"] and stale >= config["early_stopping_patience_evaluations"]:
                    stop = True
                    break
                if max_optimizer_steps is not None and total_steps >= max_steps:
                    limit_reached = True
                    break
            if stop or limit_reached:
                break
        torch.cuda.synchronize(device)
        result["completed_optimizer_steps"] = total_steps
        result["planned_optimizer_steps"] = max_steps
        result["completed_epochs"] = total_steps / optimizer_steps_per_epoch
        result["early_stopped"] = stop
        result["max_step_limit_reached"] = limit_reached
        result["train_micro_seconds"] = round(train_micro_seconds, 3)
        result["evaluation_seconds"] = round(eval_seconds, 3)
        result["checkpoint_save_seconds"] = round(save_seconds, 3)
        result["gpu"]["peak_allocated_bytes"] = torch.cuda.max_memory_allocated(device)
        result["gpu"]["peak_reserved_bytes"] = torch.cuda.max_memory_reserved(device)
        result["checkpoint"] = str(checkpoint.relative_to(root))
        result["best_optimizer_step"] = best_step
        result["best_validation_accuracy"] = best_score[0]
        result["best_validation_macro_f1"] = best_score[1]
        if best_step is None:
            raise RuntimeError("Nenhuma avaliação ou checkpoint concluído")
        del model, optimizer
        torch.cuda.empty_cache()
        reloaded = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
        from transformers import AutoModelForSequenceClassification
        model_reloaded = AutoModelForSequenceClassification.from_pretrained(checkpoint, local_files_only=True).to(device)
        sample = reloaded.pad(
            [{key: value[index] for key, value in valid_encoded.items()} for index in range(5)],
            padding=True, return_tensors="pt",
        ).to(device)
        model_reloaded.eval()
        with torch.inference_mode():
            logits = model_reloaded(**sample).logits
        result["checkpoint_reload"] = {
            "logits_shape": list(logits.shape),
            "all_finite": bool(torch.isfinite(logits).all().item()),
            "predicted_labels": [config["labels"][index] for index in logits.argmax(dim=-1).tolist()],
        }
        if result["checkpoint_reload"]["logits_shape"] != [5, 3] or not result["checkpoint_reload"]["all_finite"]:
            raise RuntimeError("Checkpoint recarregado inválido")
        result["total_wall_seconds"] = round(time.perf_counter() - started, 3)
        (run_dir / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for field, title in (("accuracy", "Acurácia"), ("loss", "Loss")):
            curve = {
                "title": f"{candidate_id}: {title.lower()} por passo",
                "x_label": "Passo do otimizador", "y_label": title,
                "series": [
                    {"label": "Treino", "points": [[p["optimizer_step"], p["train"][field]] for p in result["history"]]},
                    {"label": "Validação", "points": [[p["optimizer_step"], (p["validation"]["metrics"]["accuracy"] if field == "accuracy" else p["validation"]["loss"])] for p in result["history"]]},
                ],
            }
            plot_series_svg(curve, root / "reports" / f"etapa{run_stage}" / f"{run_id}_{field}.svg")
        print(json.dumps({"run_id": run_id, "best_step": best_step, "best_accuracy": best_score[0], "total_wall_seconds": result["total_wall_seconds"], "peak_allocated_bytes": result["gpu"]["peak_allocated_bytes"]}, indent=2), flush=True)
        return result
    except Exception as exc:
        failure = {
            "run_id": run_id,
            "candidate": candidate_id,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "completed_optimizer_steps": total_steps,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        }
        (run_dir / "failure.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_id")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--fold", type=int, default=None)
    parser.add_argument("--full-fold", action="store_true")
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--eval-every", type=int, default=None)
    parser.add_argument("--stage", type=int, default=4)
    parser.add_argument("--train-indices-manifest", type=Path, default=None)
    args = parser.parse_args()
    run_id = args.run_id or f"stage{args.stage}_{args.candidate_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run(
        Path(__file__).resolve().parents[1], args.candidate_id, run_id,
        fold_override=args.fold, full_fold=args.full_fold,
        max_optimizer_steps=args.max_steps,
        eval_every_optimizer_steps=args.eval_every, run_stage=args.stage,
        train_indices_manifest=args.train_indices_manifest,
    )


if __name__ == "__main__":
    main()
