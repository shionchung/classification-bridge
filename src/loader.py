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
    """Legacy combined file if present."""
    return _read_excel(DATA_DIR / "nlsfb.xlsx")


def load_nlsfb_table1() -> pd.DataFrame:
    """NL-SfB Table 1 — elements by position/function (Madaster-oriented)."""
    path = DATA_DIR / "nlsfb_table1.xlsx"
    if path.exists():
        return _read_excel(path)
    return load_nlsfb()


def load_nlsfb_table3() -> pd.DataFrame:
    """NL-SfB Table 3 — materials (circularity-oriented)."""
    path = DATA_DIR / "nlsfb_table3.xlsx"
    if path.exists():
        return _read_excel(path)
    raise FileNotFoundError(
        "Missing nlsfb_table3.xlsx. Download NL-SfB Table 3 from BIM Loket — see data/README.md"
    )


def load_etim() -> pd.DataFrame:
    return _read_excel(DATA_DIR / "etim.xlsx")


def explore(df: pd.DataFrame, name: str, max_rows: int = 20) -> None:
    print(f"\n=== {name} ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head(max_rows).to_string())


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore classification Excel files")
    parser.add_argument(
        "--table",
        choices=[
            "pr",
            "ss",
            "ef",
            "nlsfb",
            "nlsfb1",
            "nlsfb3",
            "etim",
            "all",
        ],
        default="all",
    )
    parser.add_argument("--rows", type=int, default=20, help="Rows to print per table")
    args = parser.parse_args()

    loaders = {
        "pr": ("Uniclass Pr", load_uniclass_products),
        "ss": ("Uniclass Ss", load_uniclass_systems),
        "ef": ("Uniclass EF", load_uniclass_elements),
        "nlsfb": ("NL-SfB (combined)", load_nlsfb),
        "nlsfb1": ("NL-SfB Table 1 — elements", load_nlsfb_table1),
        "nlsfb3": ("NL-SfB Table 3 — materials", load_nlsfb_table3),
        "etim": ("ETIM", load_etim),
    }

    targets = loaders.keys() if args.table == "all" else [args.table]
    for key in targets:
        label, fn = loaders[key]
        try:
            explore(fn(), label, max_rows=args.rows)
        except FileNotFoundError as exc:
            print(f"\n[skip] {exc}")


if __name__ == "__main__":
    main()
