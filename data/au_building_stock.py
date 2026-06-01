"""
Load Australian building material intensities from CSV (editable without Python).

Files:
  - au_material_intensities.csv — kg/m² per building_type, era, material_key
  - au_building_stock_meta.csv — confidence and source citation per type × era

Replace PLACEHOLDER values with literature-backed figures (AHURI 402, Stephan & Crawford).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent
INTENSITIES_CSV = _DATA_DIR / "au_material_intensities.csv"
META_CSV = _DATA_DIR / "au_building_stock_meta.csv"

ERA_ORDER = [
    "pre_1960",
    "1960_1979",
    "1980_1989",
    "1990_1999",
    "2000_2004",
    "2005_2014",
    "2015_present",
]

BUILDING_TYPES = [
    "commercial_office",
    "residential_detached",
    "residential_apartment",
    "education",
    "industrial_warehouse",
]


def _load_intensities() -> dict[tuple[str, str], dict]:
    intensities = pd.read_csv(INTENSITIES_CSV)
    meta = pd.read_csv(META_CSV)

    required = {"building_type", "era", "material_key", "kg_per_m2"}
    if not required.issubset(intensities.columns):
        missing = required - set(intensities.columns)
        raise ValueError(f"{INTENSITIES_CSV.name} missing columns: {missing}")

    result: dict[tuple[str, str], dict] = {}
    for (building_type, era), group in intensities.groupby(
        ["building_type", "era"], sort=False
    ):
        block = {
            row.material_key: float(row.kg_per_m2)
            for row in group.itertuples(index=False)
        }
        meta_row = meta[
            (meta["building_type"] == building_type) & (meta["era"] == era)
        ]
        if not meta_row.empty:
            block["_confidence"] = str(meta_row.iloc[0]["confidence"])
            block["_source"] = str(meta_row.iloc[0]["source"])
        else:
            block["_confidence"] = "unknown"
            block["_source"] = "missing from au_building_stock_meta.csv"
        result[(str(building_type), str(era))] = block

    return result


MATERIAL_INTENSITIES = _load_intensities()

ERAS = [era for era in ERA_ORDER if era in {e for _, e in MATERIAL_INTENSITIES}]


def reload() -> None:
    """Reload CSV data (e.g. after editing files in a long-running process)."""
    global MATERIAL_INTENSITIES, ERAS
    MATERIAL_INTENSITIES = _load_intensities()
    ERAS = [era for era in ERA_ORDER if era in {e for _, e in MATERIAL_INTENSITIES}]
