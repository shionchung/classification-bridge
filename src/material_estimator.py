"""Estimate a material passport from basic building inputs (no BIM)."""

from __future__ import annotations

from typing import Any

from data.au_building_stock import MATERIAL_INTENSITIES
from src.mapper import ClassificationMapper


class MaterialPassportEstimator:
    def __init__(self, mapper: ClassificationMapper | None = None):
        self.mapper = mapper or ClassificationMapper()

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

        for material_name, kg_per_m2 in intensities.items():
            if material_name.startswith("_"):
                continue
            if not isinstance(kg_per_m2, (int, float)):
                continue

            total_kg = kg_per_m2 * floor_area_m2
            classification = self.mapper.search_by_material_key(material_name)
            first = classification[0] if classification else {}

            materials.append(
                {
                    "material": material_name,
                    "estimated_kg": round(total_kg, 1),
                    "kg_per_m2": kg_per_m2,
                    "uniclass_pr": first.get("uniclass_pr"),
                    "uniclass_ss": first.get("uniclass_ss"),
                    "nlsfb": first.get("nlsfb_element"),
                    "etim": first.get("etim_code"),
                    "mapping_confidence": first.get("confidence"),
                }
            )

        return {
            "building_type": building_type,
            "floor_area_m2": floor_area_m2,
            "year_built": year_built,
            "postcode": postcode,
            "era": era,
            "confidence": intensities.get("_confidence", "unknown"),
            "data_source": intensities.get("_source", "unknown"),
            "materials": materials,
            "passport_format_version": "0.1-AU",
        }

    @staticmethod
    def _year_to_era(year: int) -> str:
        if year < 1960:
            return "pre_1960"
        if year < 1980:
            return "1960_1979"
        if year < 2000:
            return "1980_1999"
        if year < 2010:
            return "2000_2009"
        return "2010_present"


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
