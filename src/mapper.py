"""Cross-jurisdiction classification lookup from manual_mappings.csv (schema v2)."""

from __future__ import annotations

import sqlite3
from typing import Any

import pandas as pd

from src.paths import DEFAULT_DB, MANUAL_MAPPINGS_CSV


def _empty(val: Any) -> bool:
    if val is None:
        return True
    if isinstance(val, float) and pd.isna(val):
        return True
    return str(val).strip() == ""


def _str_or_none(val: Any) -> str | None:
    if _empty(val):
        return None
    return str(val).strip()


class ClassificationMapper:
    def __init__(self, db_path: str | None = None, csv_path: str | None = None):
        self.db_path = str(db_path or DEFAULT_DB)
        self.csv_path = csv_path or str(MANUAL_MAPPINGS_CSV)
        self._load_mappings()

    def _load_mappings(self) -> None:
        df = pd.read_csv(self.csv_path)
        # Backward compat: rename v1 columns if present
        if "notes" in df.columns and "mapping_notes" not in df.columns:
            df = df.rename(columns={"notes": "mapping_notes"})
        conn = sqlite3.connect(self.db_path)
        df.to_sql("mappings", conn, if_exists="replace", index=False)
        conn.close()

    def uniclass_to_crosswalk(self, uniclass_code: str) -> dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        result = pd.read_sql(
            "SELECT * FROM mappings WHERE uniclass_pr = ?",
            conn,
            params=(uniclass_code,),
        )
        conn.close()

        if result.empty:
            return {"status": "not_found", "code": uniclass_code}

        return self._row_to_result(result.iloc[0], status="found")

    def uniclass_to_nlsfb(self, uniclass_code: str) -> dict[str, Any]:
        """Backward-compatible alias for API and tests."""
        return self.uniclass_to_crosswalk(uniclass_code)

    def search_by_name(self, query: str) -> list[dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        results = pd.read_sql(
            """
            SELECT * FROM mappings
            WHERE material_name LIKE ? OR material_key LIKE ?
            """,
            conn,
            params=(f"%{query}%", f"%{query}%"),
        )
        conn.close()
        return [self._row_to_dict(row) for _, row in results.iterrows()]

    def search_by_material_key(self, material_key: str) -> list[dict[str, Any]]:
        """Match estimator keys; exact material_key first, then fuzzy name."""
        key = material_key.lower().strip()
        conn = sqlite3.connect(self.db_path)
        exact = pd.read_sql(
            "SELECT * FROM mappings WHERE lower(material_key) = ?",
            conn,
            params=(key,),
        )
        if not exact.empty:
            conn.close()
            return [self._row_to_dict(row) for _, row in exact.iterrows()]

        normalized = material_key.replace("_", " ")
        results = pd.read_sql(
            """
            SELECT * FROM mappings
            WHERE lower(replace(material_name, ' ', '_')) LIKE ?
               OR lower(material_name) LIKE ?
            ORDER BY length(material_key) ASC
            """,
            conn,
            params=(f"%{key}%", f"%{normalized.lower()}%"),
        )
        conn.close()
        return [self._row_to_dict(row) for _, row in results.iterrows()]

    def list_all(self, review_status: str | None = None) -> list[dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        if review_status:
            results = pd.read_sql(
                "SELECT * FROM mappings WHERE review_status = ? ORDER BY material_name",
                conn,
                params=(review_status,),
            )
        else:
            results = pd.read_sql(
                "SELECT * FROM mappings ORDER BY material_name", conn
            )
        conn.close()
        return [self._row_to_dict(row) for _, row in results.iterrows()]

    @staticmethod
    def _row_to_dict(row: Any) -> dict[str, Any]:
        data = row.to_dict()
        # Normalise NaN for JSON
        return {k: (None if _empty(v) else v) for k, v in data.items()}

    @classmethod
    def build_classification_block(cls, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "uniclass": {
                "pr": data.get("uniclass_pr"),
                "ss": _str_or_none(data.get("uniclass_ss")),
                "edition": _str_or_none(data.get("uniclass_edition")) or "2015",
            },
            "nlsfb": {
                "element": _str_or_none(data.get("nlsfb_element")),
                "material": _str_or_none(data.get("nlsfb_material")),
                "edition": _str_or_none(data.get("nlsfb_edition")) or "2005",
            },
            "etim": {
                "code": _str_or_none(data.get("etim_code")),
                "version": _str_or_none(data.get("etim_version")) or "9",
            },
        }

    def dict_to_result(self, data: dict[str, Any], status: str = "found") -> dict[str, Any]:
        return self._row_to_result(pd.Series(data), status=status)

    def _row_to_result(self, row: Any, status: str | None = None) -> dict[str, Any]:
        data = self._row_to_dict(row)
        classification = self.build_classification_block(data)
        return {
            "status": status or "found",
            "material_key": data.get("material_key"),
            "material_name": data.get("material_name"),
            "classification": classification,
            # Flat fields for backward compatibility
            "uniclass_pr": data.get("uniclass_pr"),
            "uniclass_ss": data.get("uniclass_ss"),
            "uniclass_edition": classification["uniclass"]["edition"],
            "nlsfb_element": classification["nlsfb"]["element"],
            "nlsfb_material": classification["nlsfb"]["material"],
            "nlsfb_edition": classification["nlsfb"]["edition"],
            "etim_code": classification["etim"]["code"],
            "etim_version": classification["etim"]["version"],
            "confidence": data.get("confidence", "unknown"),
            "review_status": data.get("review_status", "draft"),
            "mapping_notes": data.get("mapping_notes") or "",
        }
