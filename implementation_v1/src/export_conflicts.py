"""Gera uma lista auditável de linhas de train.xlsx com rótulos conflitantes."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import openpyxl

from audit_and_split import EXPECTED_SHA256, digest_file, group_id, group_text


def build_report(root: Path, output: Path) -> dict:
    source = root / "train.xlsx"
    actual_hash = digest_file(source)
    if actual_hash != EXPECTED_SHA256:
        raise ValueError("train.xlsx mudou desde a auditoria; conferir a fonte antes de gerar o relatório")

    workbook = openpyxl.load_workbook(source, read_only=True, data_only=True)
    sheet = workbook["train"]
    if tuple(cell.value for cell in sheet[1]) != ("resp_text", "clarity"):
        raise ValueError("Cabeçalho inesperado em train.xlsx")

    groups = defaultdict(list)
    for excel_row, (raw_text, label) in enumerate(
        sheet.iter_rows(min_row=2, max_col=2, values_only=True), start=2
    ):
        text = raw_text if isinstance(raw_text, str) else str(raw_text)
        groups[group_id(group_text(text))].append((excel_row, label, text))
    workbook.close()

    conflicts = [
        (key, entries)
        for key, entries in groups.items()
        if len({label for _, label, _ in entries}) > 1
    ]
    conflicts.sort(key=lambda pair: pair[1][0][0])
    conflicting_rows = sum(len(entries) for _, entries in conflicts)
    exact_conflicting_groups = 0
    exact_conflicting_variants = 0
    lines = [
        "# Linhas de treino com rótulos conflitantes",
        "",
        f"Gerado em {datetime.now().astimezone().strftime('%d/%m/%Y %H:%M %Z')} a partir de `train.xlsx`, aba `train`.",
        f"SHA-256 do arquivo: `{actual_hash}`.",
        "",
        f"Foram encontrados **{len(conflicts)} grupos** com mais de um rótulo, somando **{conflicting_rows} linhas**. "
        "Os números abaixo são as **linhas visíveis no Excel**, incluindo o cabeçalho na linha 1. "
        "Abra `train.xlsx` e compare `resp_text` e `clarity` nas linhas indicadas.",
        "",
        "## Como os grupos foram identificados",
        "",
        "Duas respostas entraram no mesmo grupo após normalizar Unicode para NFC, ignorar diferenças "
        "de maiúsculas/minúsculas e reduzir sequências de espaços a um espaço. "
        "O texto e os rótulos originais da planilha **não foram modificados**. "
        "A coluna **Conflito literal** indica se ao menos duas células com texto exatamente igual "
        "já possuem rótulos diferentes. Quando está como `Não`, a divergência aparece apenas depois "
        "da normalização descrita.",
        "",
        "O documento lista linhas e rótulos, sem copiar o conteúdo integral das respostas. "
        "Ele deve ser consultado junto à planilha original.",
        "",
        "## Exemplo simples",
        "",
        "A resposta `Prezado,` aparece nas linhas Excel 2836, 6933, 12545, 14059, 15874, "
        "16074 e 16461, com quatro rótulos `c5`, dois `c1` e um `c234`. "
        "Algumas células diferem apenas na quantidade de espaços; outras são literalmente iguais.",
        "",
        "## Lista completa",
        "",
        "| Grupo | Linhas | Conflito literal | Linhas com `c1` | Linhas com `c234` | Linhas com `c5` |",
        "| --- | ---: | :---: | --- | --- | --- |",
    ]

    for number, (_, entries) in enumerate(conflicts, start=1):
        by_label = defaultdict(list)
        by_exact = defaultdict(set)
        for row, label, text in entries:
            by_label[label].append(row)
            by_exact[text].add(label)
        variant_conflicts = sum(len(label_set) > 1 for label_set in by_exact.values())
        literal_conflict = variant_conflicts > 0
        exact_conflicting_groups += literal_conflict
        exact_conflicting_variants += variant_conflicts
        cells = [", ".join(map(str, by_label[label])) or "—" for label in ("c1", "c234", "c5")]
        lines.append(
            f"| G{number:03d} | {len(entries)} | {'Sim' if literal_conflict else 'Não'} | "
            + " | ".join(cells)
            + " |"
        )

    lines += [
        "",
        "## Interpretação e consulta ao professor",
        "",
        f"Em {exact_conflicting_groups} grupos, existem {exact_conflicting_variants} variantes de resposta **literalmente idêntica** "
        "com rótulos diferentes. Isso pode ser esperado se cada linha representar a avaliação "
        "independente de uma pessoa, pois clareza é subjetiva. Também pode indicar problemas "
        "de anotação ou de exportação. A planilha sozinha não permite distinguir essas causas.",
        "",
        "Para um modelo que recebe apenas o texto, rótulos diferentes para a mesma resposta "
        "fornecem sinais contraditórios durante o treino e podem reduzir a acurácia máxima "
        "observável nesses casos. O impacto real no desempenho ainda precisa ser medido; "
        "este relatório não quantifica uma queda de acurácia nem justifica excluir linhas por conta própria.",
        "",
        "**Pergunta sugerida:** esses registros são avaliações independentes de usuários, "
        "devem permanecer como exemplos separados ou há uma regra oficial para corrigir/agregar "
        "rótulos de respostas repetidas?",
        "",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return {
        "groups": len(conflicts),
        "rows": conflicting_rows,
        "groups_with_exact_text_conflicts": exact_conflicting_groups,
        "exact_text_variants_with_conflicting_labels": exact_conflicting_variants,
        "output": str(output),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("reports/conflitos_rotulos_train.md"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output if args.output.is_absolute() else root / args.output
    print(json.dumps(build_report(root, output), ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
