#!/usr/bin/env python3
"""Export empty mapping curation template for Google Sheets."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "mappings" / "mapping_curation_template.csv"

COLUMNS = [
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

EXAMPLE = {
    "material_key": "structural_steel",
    "material_name": "Structural steel I-beam",
    "uniclass_pr": "Pr_20_93_74_16",
    "uniclass_ss": "Ss_25_13_70",
    "uniclass_edition": "2015",
    "nlsfb_element": "28.21",
    "nlsfb_material": "Q5",
    "nlsfb_edition": "2005",
    "etim_code": "EC001719",
    "etim_version": "9",
    "confidence": "medium",
    "review_status": "draft",
    "mapping_notes": "Table 1 = load-bearing steel structure; Table 3 Q5 = steel/iron",
    "fuzzy_match_score": "",
}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerow(EXAMPLE)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
