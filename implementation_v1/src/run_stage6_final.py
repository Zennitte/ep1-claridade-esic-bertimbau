"""Treino integral do modelo final conforme a configuração congelada na etapa 5e."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import random
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding

from audit_and_split import digest_file
from bert_stage3 import EncodedDataset, read_dataset

FROZEN_CONFIG_SHA256 = "4377c55014be7f6f3de1b89b9dfb9c64785561b3df1a4b96b4eeef7e9a8b0953"
SPLIT_SHA256 = "aa9c99a79ccccc3655399761c53098f5fd3d770c9aa6c8b68be29c49eba3586b"
ROW_MANIFEST_SHA256 = "e07917a05f89f9940d6194d118fed7ebce9b9342acfc956eb38cadfd4dc2a2c4"


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path, run_id: str) -> dict:
    config_path = root / "configs" / "bert_stage5_final.json"
    if digest_file(config_path) != FROZEN_CONFIG_SHA256:
        raise ValueError("A configuração congelada da 5e foi modificada")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    split_path = root / "data" / "splits_grouped_v1.json"
    if digest_file(split_path) != SPLIT_SHA256:
        raise ValueError("A divisão persistida foi modificada após a auditoria")
    if digest_file(root / "data" / "row_manifest.csv") != ROW_MANIFEST_SHA256:
        raise ValueError("O manifesto de grupos foi modificado após a auditoria")
    source_path = root / config["source"]["path"]
    if digest_file(source_path) != config["source"]["sha256"]:
        raise ValueError("A fonte não corresponde à especificação congelada")

    run_dir = root / "runs" / "etapa6" / run_id
    final_dir = root / "models" / "bert_final"
    training_report_dir = root / "reports" / "etapa6"
    if run_dir.exists() or final_dir.exists():
        raise FileExistsError("Run ou modelo final já existe; não sobrescrever")
    if not torch.cuda.is_available():
        raise RuntimeError("GPU ROCm indisponível")

    model_config = config["model"]
    train_config = config["training"]
    classes = [model_config["id_to_label"][str(i)] for i in range(model_config["num_labels"])]
    label2id = {name: i for i, name in enumerate(classes)}
    id2label = {i: name for name, i in label2id.items()}

    split = json.loads(split_path.read_text(encoding="utf-8"))
    text, labels = read_dataset(root, split)
    if len(text) != config["source"]["rows"] or len(labels) != len(text):
        raise ValueError("Quantidade de linhas lidas diverge da configuração congelada")
    if any(label not in label2id for label in labels):
        raise ValueError("Há rótulos fora do mapeamento congelado")
    counts = {name: labels.count(name) for name in classes}
    if counts != config["source"]["class_counts"]:
        raise ValueError(f"Distribuição de classes diverge: {counts}")
    indices = list(range(len(text)))
    steps_per_epoch = len(indices) // train_config["effective_batch_size"]
    target_steps = train_config["target_optimizer_steps"]
    accumulation = train_config["gradient_accumulation_steps"]
    if (len(indices), steps_per_epoch, target_steps, accumulation) != (20092, 2511, 4523, 4):
        raise ValueError("Contagem ou duração difere do plano congelado")

    run_dir.mkdir(parents=True, exist_ok=False)
    training_report_dir.mkdir(parents=True, exist_ok=True)
    final_dir.mkdir(parents=True, exist_ok=False)
    with (run_dir / "train_indices.csv").open("w", encoding="utf-8", newline="") as f:
        f.write("row_index,excel_row\n")
        f.writelines(f"{i},{i + 2}\n" for i in indices)

    device = torch.device("cuda:0")
    gpu = torch.cuda.get_device_properties(device)
    torch.manual_seed(train_config["seed"])
    np.random.seed(train_config["seed"])
    random.seed(train_config["seed"])
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats(device)

    result = {
        "stage": 6,
        "run_id": run_id,
        "status": "training",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "frozen_config_path": "configs/bert_stage5_final.json",
        "frozen_config_sha256": digest_file(config_path),
        "source_sha256": digest_file(source_path),
        "split_sha256": digest_file(split_path),
        "row_manifest_sha256": digest_file(root / "data" / "row_manifest.csv"),
        "train_rows": len(indices),
        "class_counts": counts,
        "train_indices_path": "train_indices.csv",
        "train_indices_sha256": sha256(run_dir / "train_indices.csv"),
        "holdout_re_evaluated": False,
        "test_xlsx_accessed": False,
        "training": {
            **train_config,
            "actual_steps_per_epoch": steps_per_epoch,
            "actual_epoch_equivalents": target_steps / steps_per_epoch,
        },
        "model": model_config,
        "gpu": {"name": gpu.name, "total_memory_bytes": gpu.total_memory},
        "versions": {name: version(name) for name in ("torch", "transformers", "tokenizers", "openpyxl")},
    }
    save_json(run_dir / "run.json", result)
    (run_dir / "config.json").write_bytes(config_path.read_bytes())

    tokenizer = AutoTokenizer.from_pretrained(
        model_config["tokenizer_id"], revision=model_config["tokenizer_revision"], local_files_only=True
    )
    encoded = tokenizer(
        text, truncation=True, max_length=model_config["max_length_including_special_tokens"], padding=False
    )
    dataset = EncodedDataset(encoded, [label2id[name] for name in labels])
    generator = torch.Generator().manual_seed(train_config["shuffle_generator_seed"])
    loader = DataLoader(
        dataset, batch_size=train_config["micro_batch_size"], shuffle=True, generator=generator,
        num_workers=train_config["num_workers"],
        collate_fn=DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt"),
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        model_config["pretrained_model_id"], revision=model_config["pretrained_model_revision"],
        num_labels=len(classes), label2id=label2id, id2label=id2label, local_files_only=True,
    ).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=train_config["learning_rate"],
        betas=tuple(train_config["adam_betas"]), eps=train_config["adam_epsilon"],
        weight_decay=train_config["weight_decay"],
    )

    start = time.perf_counter()
    log_path = run_dir / "training.jsonl"
    micro_batches_per_epoch = steps_per_epoch * accumulation
    completed_steps = 0
    last_loss = None
    with log_path.open("w", encoding="utf-8") as log:
        while completed_steps < target_steps:
            model.train()
            optimizer.zero_grad(set_to_none=True)
            for batch_index, batch in enumerate(loader):
                if batch_index >= micro_batches_per_epoch:
                    break
                batch = {key: value.to(device) for key, value in batch.items()}
                output = model(**batch)
                last_loss = float(output.loss.item())
                (output.loss / accumulation).backward()
                if (batch_index + 1) % accumulation == 0:
                    torch.nn.utils.clip_grad_norm_(model.parameters(), train_config["gradient_clip_norm"])
                    optimizer.step()
                    optimizer.zero_grad(set_to_none=True)
                    completed_steps += 1
                    if completed_steps % 100 == 0 or completed_steps == target_steps:
                        torch.cuda.synchronize(device)
                        record = {
                            "step": completed_steps,
                            "epoch_equivalent": completed_steps / steps_per_epoch,
                            "last_microbatch_loss": last_loss,
                            "elapsed_seconds": round(time.perf_counter() - start, 2),
                        }
                        line = json.dumps(record)
                        log.write(line + "\n")
                        log.flush()
                        print(line, flush=True)
                    if completed_steps >= target_steps:
                        break

    torch.cuda.synchronize(device)
    result.update({
        "status": "trained_saved_validating",
        "training_completed_utc": datetime.now(timezone.utc).isoformat(),
        "optimizer_steps_completed": completed_steps,
        "last_microbatch_loss": last_loss,
        "training_seconds": round(time.perf_counter() - start, 3),
        "peak_gpu_memory_bytes": torch.cuda.max_memory_allocated(device),
    })
    model.save_pretrained(final_dir, safe_serialization=True)
    tokenizer.save_pretrained(final_dir)
    result["model_files_sha256"] = {
        p.name: digest_file(p) for p in sorted(final_dir.iterdir()) if p.is_file()
    }
    save_json(run_dir / "run.json", result)

    # Reload and validate determinism and probability shape on five development rows.
    sample_indices = [0, 1, 2, len(text) // 2, len(text) - 1]
    sample_tokens = tokenizer(
        [text[i] for i in sample_indices], truncation=True,
        max_length=model_config["max_length_including_special_tokens"], padding=False,
    )
    sample_batch = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")(
        [{key: sample_tokens[key][j] for key in sample_tokens} for j in range(len(sample_indices))]
    )
    del optimizer, model
    gc.collect()
    torch.cuda.empty_cache()
    reloaded = AutoModelForSequenceClassification.from_pretrained(final_dir, local_files_only=True).to(device)
    reloaded.eval()
    sample_batch = {key: value.to(device) for key, value in sample_batch.items()}
    with torch.inference_mode():
        logits1 = reloaded(**sample_batch).logits
        logits2 = reloaded(**sample_batch).logits
        probs = logits1.softmax(dim=-1)
    torch.cuda.synchronize(device)
    predictions1 = logits1.argmax(dim=-1)
    predictions2 = logits2.argmax(dim=-1)
    deterministic = torch.equal(predictions1, predictions2)
    probabilities_valid = (
        tuple(probs.shape) == (len(sample_indices), len(classes))
        and bool(torch.isfinite(probs).all())
        and bool(torch.allclose(probs.sum(dim=-1), torch.ones(len(sample_indices), device=device), atol=1e-6))
    )
    predicted = [classes[i] for i in probs.argmax(dim=-1).tolist()]
    reload_ok = deterministic and probabilities_valid and set(predicted).issubset(set(classes))
    result["reload_validation"] = {
        "rows": len(sample_indices),
        "row_indices": sample_indices,
        "logits_shape": list(logits1.shape),
        "probabilities_shape": list(probs.shape),
        "probabilities_finite_and_sum_to_one": probabilities_valid,
        "repeat_predictions_identical": deterministic,
        "predicted_classes": predicted,
        "all_classes_in_frozen_mapping": set(predicted).issubset(set(classes)),
        "passed": reload_ok,
    }
    result["status"] = "complete" if reload_ok else "validation_failed"
    result["completed_utc"] = datetime.now(timezone.utc).isoformat()
    save_json(run_dir / "run.json", result)
    save_json(training_report_dir / f"{run_id}_summary.json", result)
    if not reload_ok:
        raise RuntimeError("A validação de recarga do modelo final falhou")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    result = run(args.root.resolve(), args.run_id)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
