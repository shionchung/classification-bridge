"""Estimate a material passport from basic building inputs (no BIM)."""

from __future__ import annotations

from typing import Any

from data.au_building_stock import MATERIAL_INTENSITIES
from src.mapper import ClassificationMapper


class MaterialPassportEstimator:
    def __init__(
        self,
        mapper: ClassificationMapper | None = None,
        *,
        legacy_flat_codes: bool = True,
    ):
        self.mapper = mapper or ClassificationMapper()
        self.legacy_flat_codes = legacy_flat_codes

    def estimate(
        self,
        building_type: str,
        floor_area_m2: float,
        year_built: int,
        postcode: str | None = None,
    ) -> dict[str, Any]:
        era = self._year_to_era(year_built)
        key = (building_type, era)

        if key not in MATERIAL_INTENSITIES:
            return {
                "error": f"No data for {building_type} built in {era}",
                "building_type": building_type,
                "year_built": year_built,
                "era": era,
                "available_keys": sorted(
                    f"{bt}/{e}" for bt, e in MATERIAL_INTENSITIES.keys()
                ),
            }

        intensities = MATERIAL_INTENSITIES[key]
        materials = []
        unverified_mappings = 0

        for material_name, kg_per_m2 in intensities.items():
            if material_name.startswith("_"):
                continue
            if not isinstance(kg_per_m2, (int, float)):
                continue

            total_kg = kg_per_m2 * floor_area_m2
            classification_rows = self.mapper.search_by_material_key(material_name)
            first = classification_rows[0] if classification_rows else {}
            block = (
                ClassificationMapper.build_classification_block(first)
                if first
                else {
                    "uniclass": {"pr": None, "ss": None, "edition": "2015"},
                    "nlsfb": {"element": None, "material": None, "edition": "2005"},
                    "etim": {"code": None, "version": "9"},
                }
            )
            review_status = first.get("review_status") or "missing"
            if review_status != "verified":
                unverified_mappings += 1

            row: dict[str, Any] = {
                "material": material_name,
                "estimated_kg": round(total_kg, 1),
                "kg_per_m2": kg_per_m2,
                "classification": block,
                "mapping_confidence": first.get("confidence"),
                "mapping_review_status": review_status,
            }

            if self.legacy_flat_codes:
                row["uniclass_pr"] = block["uniclass"]["pr"]
                row["uniclass_ss"] = block["uniclass"]["ss"]
                row["nlsfb"] = block["nlsfb"]["element"]
                row["nlsfb_element"] = block["nlsfb"]["element"]
                row["nlsfb_material"] = block["nlsfb"]["material"]
                row["etim"] = block["etim"]["code"]

            materials.append(row)

        return {
            "building_type": building_type,
            "floor_area_m2": floor_area_m2,
            "year_built": year_built,
            "postcode": postcode,
            "era": era,
            "confidence": intensities.get("_confidence", "unknown"),
            "data_source": intensities.get("_source", "unknown"),
            "materials": materials,
            "passport_format_version": "0.2-AU",
            "mapping_summary": {
                "total_materials": len(materials),
                "unverified_mappings": unverified_mappings,
            },
        }

    @staticmethod
    def _year_to_era(year: int) -> str:
        """Era buckets aligned to shifts ~1980 and ~2005 in AU construction practice."""
        if year < 1960:
            return "pre_1960"
        if year < 1980:
            return "1960_1979"
        if year < 1990:
            return "1980_1989"
        if year < 2000:
            return "1990_1999"
        if year < 2005:
            return "2000_2004"
        if year < 2015:
            return "2005_2014"
        return "2015_present"


def main() -> None:
    estimator = MaterialPassportEstimator()
    passport = estimator.estimate(
        building_type="commercial_office",
        floor_area_m2=3500,
        year_built=1987,
    )
    import json

    print(json.dumps(passport, indent=2))


if __name__ == "__main__":
    main()
