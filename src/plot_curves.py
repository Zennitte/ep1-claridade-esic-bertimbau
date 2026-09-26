"""Gera gráficos SVG de séries numéricas para os experimentos do projeto."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path


COLORS = ("#1769aa", "#e07a26", "#27854d", "#a33a8e", "#777777")


def plot_series_svg(spec: dict, output: Path) -> None:
    series = spec["series"]
    points = [(float(x), float(y)) for item in series for x, y in item["points"]]
    if not points:
        raise ValueError("O gráfico precisa de pontos")
    width, height = 900, 540
    left, top, right, bottom = 90, 70, 55, 85
    x_min, x_max = min(x for x, _ in points), max(x for x, _ in points)
    y_min, y_max = min(y for _, y in points), max(y for _, y in points)
    if x_min == x_max:
        x_min -= 1
        x_max += 1
    if y_min == y_max:
        y_min -= 0.01
        y_max += 0.01
    else:
        pad = (y_max - y_min) * 0.1
        y_min -= pad
        y_max += pad

    def px(x: float) -> float:
        return left + (x - x_min) / (x_max - x_min) * (width - left - right)

    def py(y: float) -> float:
        return height - bottom - (y - y_min) / (y_max - y_min) * (height - top - bottom)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold">{escape(spec["title"])}</text>',
    ]
    for tick in range(6):
        y_value = y_min + (y_max - y_min) * tick / 5
        y = py(y_value)
        svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#e8edf2"/>')
        svg.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="13">{y_value:.3f}</text>')
    for tick in range(6):
        x_value = x_min + (x_max - x_min) * tick / 5
        x = px(x_value)
        svg.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" stroke="#f1f3f5"/>')
        svg.append(f'<text x="{x:.1f}" y="{height-bottom+25}" text-anchor="middle" font-family="Arial" font-size="13">{x_value:.2g}</text>')
    svg.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#34495e" stroke-width="2"/>')
    svg.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#34495e" stroke-width="2"/>')
    for index, item in enumerate(series):
        color = COLORS[index % len(COLORS)]
        ordered = sorted((float(x), float(y)) for x, y in item["points"])
        polyline = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in ordered)
        svg.append(f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="3"/>')
        for x, y in ordered:
            svg.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="5" fill="{color}"/>')
        legend_x = left + index * (160 if len(series) > 4 else 215)
        svg.append(f'<circle cx="{legend_x}" cy="{height-22}" r="5" fill="{color}"/>')
        svg.append(f'<text x="{legend_x+12}" y="{height-17}" font-family="Arial" font-size="13">{escape(item["label"])}</text>')
    svg.append(f'<text x="{width/2}" y="{height-48}" text-anchor="middle" font-family="Arial" font-size="15">{escape(spec["x_label"])}</text>')
    svg.append(f'<text x="22" y="{height/2}" text-anchor="middle" transform="rotate(-90 22 {height/2})" font-family="Arial" font-size="15">{escape(spec["y_label"])}</text>')
    svg.append("</svg>")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(svg) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON com title, x_label, y_label e series")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    plot_series_svg(json.loads(args.input.read_text(encoding="utf-8")), args.output)


if __name__ == "__main__":
    main()
