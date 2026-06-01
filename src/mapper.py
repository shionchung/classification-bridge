"""Cross-jurisdiction classification lookup from manual_mappings.csv."""

from __future__ import annotations

import sqlite3
from typing import Any

import pandas as pd

from src.paths import DEFAULT_DB, MANUAL_MAPPINGS_CSV


class ClassificationMapper:
    def __init__(self, db_path: str | None = None, csv_path: str | None = None):
        self.db_path = str(db_path or DEFAULT_DB)
        self.csv_path = csv_path or str(MANUAL_MAPPINGS_CSV)
        self._load_mappings()

    def _load_mappings(self) -> None:
        df = pd.read_csv(self.csv_path)
        conn = sqlite3.connect(self.db_path)
        df.to_sql("mappings", conn, if_exists="replace", index=False)
        conn.close()

    def uniclass_to_nlsfb(self, uniclass_code: str) -> dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        result = pd.read_sql(
            "SELECT * FROM mappings WHERE uniclass_pr = ?",
            conn,
            params=(uniclass_code,),
        )
        conn.close()

        if result.empty:
            return {"status": "not_found", "code": uniclass_code}

        row = result.iloc[0]
        return self._row_to_result(row, status="found")

    def search_by_name(self, query: str) -> list[dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        results = pd.read_sql(
            "SELECT * FROM mappings WHERE material_name LIKE ?",
            conn,
            params=(f"%{query}%",),
        )
        conn.close()
        return [self._row_to_dict(row) for _, row in results.iterrows()]

    def search_by_material_key(self, material_key: str) -> list[dict[str, Any]]:
        """Match estimator keys (e.g. structural_steel) to CSV material_name."""
        normalized = material_key.replace("_", " ")
        conn = sqlite3.connect(self.db_path)
        results = pd.read_sql(
            """
            SELECT * FROM mappings
            WHERE lower(replace(material_name, ' ', '_')) LIKE ?
               OR lower(material_name) LIKE ?
            """,
            conn,
            params=(f"%{material_key.lower()}%", f"%{normalized.lower()}%"),
        )
        conn.close()
        return [self._row_to_dict(row) for _, row in results.iterrows()]

    def list_all(self) -> list[dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        results = pd.read_sql("SELECT * FROM mappings ORDER BY material_name", conn)
        conn.close()
        return [self._row_to_dict(row) for _, row in results.iterrows()]

    @staticmethod
    def _row_to_dict(row: Any) -> dict[str, Any]:
        return row.to_dict()

    def _row_to_result(self, row: Any, status: str | None = None) -> dict[str, Any]:
        data = self._row_to_dict(row)
        return {
            "status": status or "found",
            "material_name": data.get("material_name"),
            "uniclass_pr": data.get("uniclass_pr"),
            "uniclass_ss": data.get("uniclass_ss"),
            "nlsfb_element": data.get("nlsfb_element"),
            "etim_code": data.get("etim_code"),
            "confidence": data.get("confidence", "unknown"),
            "notes": data.get("notes", ""),
        }
