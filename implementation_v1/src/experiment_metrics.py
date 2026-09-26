"""Métricas comuns aos baselines e aos futuros modelos neurais."""

from __future__ import annotations

from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score


def classification_metrics(y_true, y_pred, classes: list[str]) -> dict:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=classes, average="macro", zero_division=0)),
        "recall_by_class": {
            label: float(value)
            for label, value in zip(
                classes,
                recall_score(y_true, y_pred, labels=classes, average=None, zero_division=0),
            )
        },
        "confusion_matrix_rows_true_columns_predicted": confusion_matrix(
            y_true, y_pred, labels=classes
        ).tolist(),
    }
