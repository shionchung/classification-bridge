#!/usr/bin/env python3
"""One-off migration: manual_mappings.csv v1 -> schema v2."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "mappings" / "manual_mappings.csv"

# material_name substring -> material_key
KEY_HINTS = [
    ("structural steel", "structural_steel"),
    ("reinforced concrete in-situ", "reinforced_concrete"),
    ("precast concrete", "precast_concrete"),
    ("softwood timber", "softwood_timber"),
    ("engineered timber", "engineered_timber"),
    ("brick clay", "brick_clay"),
    ("concrete masonry", "concrete_masonry"),
    ("float glass", "float_glass"),
    ("aluminium framing", "aluminium"),
    ("aluminium cladding", "aluminium_cladding"),
    ("plasterboard", "plasterboard"),
    ("mineral wool", "mineral_wool"),
    ("eps insulation", "eps_insulation"),
    ("copper pipe", "copper"),
    ("pvc pipe", "pvc"),
    ("galvanised steel", "galvanised_steel"),
    ("portland cement", "portland_cement"),
    ("ceramic tile", "ceramic_tile"),
    ("carpet", "carpet"),
    ("vinyl flooring", "vinyl_flooring"),
]

V2_COLUMNS = [
    "material_key",
    "material_name",
    "uniclass_pr",
    "uniclass_ss",
    "uniclass_edition",
    "nlsfb_element",
    "nlsfb_material",
    "nlsfb_edition",
    "etim_code",
    "etim_version",
    "confidence",
    "review_status",
    "mapping_notes",
    "fuzzy_match_score",
]


def infer_material_key(material_name: str) -> str:
    lower = material_name.lower()
    for hint, key in KEY_HINTS:
        if hint in lower:
            return key
    return lower.replace(" ", "_").replace("-", "_")[:64]


def migrate_row(row: dict) -> dict:
    notes = row.get("mapping_notes") or row.get("notes") or ""
    return {
        "material_key": row.get("material_key") or infer_material_key(row["material_name"]),
        "material_name": row["material_name"],
        "uniclass_pr": row["uniclass_pr"],
        "uniclass_ss": row.get("uniclass_ss", ""),
        "uniclass_edition": row.get("uniclass_edition", "2015"),
        "nlsfb_element": row.get("nlsfb_element", ""),
        "nlsfb_material": row.get("nlsfb_material", ""),
        "nlsfb_edition": row.get("nlsfb_edition", "2005"),
        "etim_code": row.get("etim_code", ""),
        "etim_version": row.get("etim_version", "9"),
        "confidence": row.get("confidence", "low"),
        "review_status": row.get("review_status", "draft"),
        "mapping_notes": notes,
        "fuzzy_match_score": row.get("fuzzy_match_score", ""),
    }


def main() -> int:
    if not CSV_PATH.exists():
        print(f"Missing {CSV_PATH}", file=sys.stderr)
        return 1

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if rows and "material_key" in rows[0] and "mapping_notes" in rows[0]:
        print("Already schema v2; no migration needed.")
        return 0

    out_rows = [migrate_row(r) for r in rows]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=V2_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Migrated {len(out_rows)} rows -> {CSV_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
