#!/usr/bin/env python3
"""
Suggest Uniclass Pr -> ETIM candidate pairs (review only; never writes manual_mappings.csv).

Requires: data/uniclass_pr.xlsx, data/etim.xlsx
Output: mappings/etim_candidates.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "mappings" / "etim_candidates.csv"
WATCHLIST = ROOT / "mappings" / "core_material_watchlist.txt"


def _pick_label_column(df: pd.DataFrame) -> str:
    for col in df.columns:
        lower = str(col).lower()
        if any(k in lower for k in ("title", "description", "name", "label")):
            return col
    return str(df.columns[0])


def _pick_code_column(df: pd.DataFrame, prefix: str) -> str:
    for col in df.columns:
        series = df[col].astype(str)
        if series.str.contains(prefix, case=False, na=False).any():
            return col
    return str(df.columns[0])


def load_labels(path: Path, code_prefix: str) -> list[tuple[str, str]]:
    df = pd.read_excel(path)
    code_col = _pick_code_column(df, code_prefix)
    label_col = _pick_label_column(df)
    pairs = []
    for _, row in df.iterrows():
        code = str(row[code_col]).strip()
        label = str(row[label_col]).strip()
        if code and code != "nan" and label and label != "nan":
            pairs.append((code, label))
    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description="Fuzzy-match Uniclass Pr to ETIM candidates")
    parser.add_argument("--min-score", type=int, default=60, help="Minimum rapidfuzz score 0-100")
    parser.add_argument("--top", type=int, default=3, help="Top ETIM matches per Uniclass row")
    args = parser.parse_args()

    pr_path = DATA / "uniclass_pr.xlsx"
    etim_path = DATA / "etim.xlsx"
    if not pr_path.exists() or not etim_path.exists():
        print("Missing uniclass_pr.xlsx or etim.xlsx in data/", file=sys.stderr)
        return 1

    try:
        from rapidfuzz import fuzz, process
    except ImportError:
        print("Install dev deps: pip install -r requirements-dev.txt", file=sys.stderr)
        return 1

    uniclass = load_labels(pr_path, "Pr_")
    etim = load_labels(etim_path, "EC")
    etim_labels = [label for _, label in etim]
    etim_by_label = {label: code for code, label in etim}

    if WATCHLIST.exists():
        watch = {
            line.strip().lower()
            for line in WATCHLIST.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }
        uniclass = [(c, l) for c, l in uniclass if any(w in l.lower() or w in c.lower() for w in watch)]

    rows: list[dict] = []
    for pr_code, pr_label in uniclass:
        matches = process.extract(
            pr_label,
            etim_labels,
            scorer=fuzz.token_sort_ratio,
            limit=args.top,
        )
        for etim_label, score, _ in matches:
            if score < args.min_score:
                continue
            rows.append(
                {
                    "uniclass_pr": pr_code,
                    "uniclass_title": pr_label,
                    "etim_code": etim_by_label.get(etim_label, ""),
                    "etim_title": etim_label,
                    "score": score,
                    "review_status": "draft",
                }
            )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "uniclass_pr",
        "uniclass_title",
        "etim_code",
        "etim_title",
        "score",
        "review_status",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} candidates to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
