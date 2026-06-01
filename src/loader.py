"""Load and explore classification spreadsheets from data/."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.paths import DATA_DIR


def _read_excel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path.name}. Download sources listed in data/README.md"
        )
    return pd.read_excel(path)


def load_uniclass_products() -> pd.DataFrame:
    return _read_excel(DATA_DIR / "uniclass_pr.xlsx")


def load_uniclass_systems() -> pd.DataFrame:
    return _read_excel(DATA_DIR / "uniclass_ss.xlsx")


def load_uniclass_elements() -> pd.DataFrame:
    return _read_excel(DATA_DIR / "uniclass_ef.xlsx")


def load_nlsfb() -> pd.DataFrame:
    return _read_excel(DATA_DIR / "nlsfb.xlsx")


def load_etim() -> pd.DataFrame:
    return _read_excel(DATA_DIR / "etim.xlsx")


def explore(df: pd.DataFrame, name: str) -> None:
    print(f"\n=== {name} ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head(20).to_string())


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore classification Excel files")
    parser.add_argument(
        "--table",
        choices=["pr", "ss", "ef", "nlsfb", "etim", "all"],
        default="all",
    )
    args = parser.parse_args()

    loaders = {
        "pr": ("Uniclass Pr", load_uniclass_products),
        "ss": ("Uniclass Ss", load_uniclass_systems),
        "ef": ("Uniclass EF", load_uniclass_elements),
        "nlsfb": ("NL-SfB", load_nlsfb),
        "etim": ("ETIM", load_etim),
    }

    targets = loaders.keys() if args.table == "all" else [args.table]
    for key in targets:
        label, fn = loaders[key]
        try:
            explore(fn(), label)
        except FileNotFoundError as exc:
            print(f"\n[skip] {exc}")


if __name__ == "__main__":
    main()
