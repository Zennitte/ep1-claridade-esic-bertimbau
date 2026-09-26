"""Classifica textos com o modelo final salvo em models/bert_final/."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", action="append", required=True, help="Texto a classificar; pode repetir a opção")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    model_dir = root / "models" / "bert_final"
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("GPU CUDA/ROCm não está disponível")
    device = torch.device("cuda:0" if args.device == "cuda" or (args.device == "auto" and torch.cuda.is_available()) else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir, local_files_only=True).to(device)
    model.eval()

    encoded = tokenizer(args.text, truncation=True, max_length=512, padding=False)
    collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")
    features = [{key: encoded[key][i] for key in encoded} for i in range(len(args.text))]
    batch = {key: value.to(device) for key, value in collator(features).items()}
    with torch.inference_mode():
        probs = model(**batch).logits.softmax(dim=-1).cpu()
    id2label = {int(index): label for index, label in model.config.id2label.items()}
    results = []
    for text, row in zip(args.text, probs.tolist()):
        pred_id = max(range(len(row)), key=row.__getitem__)
        results.append({
            "text": text,
            "predicted_label": id2label[pred_id],
            "probabilities": {id2label[i]: row[i] for i in range(len(row))},
        })
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
