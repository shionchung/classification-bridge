"""Sanity checks for material passport JSON shape and arithmetic."""

from __future__ import annotations

import pytest

from src.material_estimator import MaterialPassportEstimator

PASSPORT_TOP_KEYS = {
    "building_type",
    "floor_area_m2",
    "year_built",
    "era",
    "confidence",
    "data_source",
    "materials",
    "passport_format_version",
    "mapping_summary",
}

CLASSIFICATION_KEYS = {"uniclass", "nlsfb", "etim"}


@pytest.mark.parametrize(
    "year,expected_era",
    [
        (1955, "pre_1960"),
        (1970, "1960_1979"),
        (1987, "1980_1989"),
        (1995, "1990_1999"),
        (2003, "2000_2004"),
        (2010, "2005_2014"),
        (2020, "2015_present"),
    ],
)
def test_year_to_era(year, expected_era):
    assert MaterialPassportEstimator._year_to_era(year) == expected_era


def test_estimate_returns_passport_v02(estimator):
    passport = estimator.estimate(
        building_type="commercial_office",
        floor_area_m2=3500,
        year_built=1987,
    )
    assert "error" not in passport
    assert set(passport.keys()) >= PASSPORT_TOP_KEYS
    assert passport["passport_format_version"] == "0.2-AU"
    assert passport["era"] == "1980_1989"
    assert len(passport["materials"]) > 0


def test_estimate_material_row_has_nested_classification(estimator):
    passport = estimator.estimate(
        building_type="commercial_office",
        floor_area_m2=100,
        year_built=1987,
    )
    row = passport["materials"][0]
    assert set(row["classification"].keys()) == CLASSIFICATION_KEYS
    assert "element" in row["classification"]["nlsfb"]
    assert "material" in row["classification"]["nlsfb"]
    assert "mapping_review_status" in row


def test_estimate_kg_arithmetic_and_dual_nlsfb(estimator):
    passport = estimator.estimate(
        building_type="commercial_office",
        floor_area_m2=3500,
        year_built=1987,
    )
    steel = next(m for m in passport["materials"] if m["material"] == "structural_steel")
    assert steel["kg_per_m2"] == 52
    assert steel["estimated_kg"] == 182000.0
    assert steel["classification"]["uniclass"]["pr"] == "Pr_20_93_74_16"
    assert steel["classification"]["etim"]["code"] == "EC001719"
    assert steel["classification"]["nlsfb"]["element"] == "28.21"
    assert steel["classification"]["nlsfb"]["material"] == "Q5"
    assert steel["mapping_review_status"] == "verified"


def test_legacy_flat_codes_when_enabled(estimator):
    passport = MaterialPassportEstimator(legacy_flat_codes=True).estimate(
        building_type="commercial_office",
        floor_area_m2=100,
        year_built=1987,
    )
    steel = next(m for m in passport["materials"] if m["material"] == "structural_steel")
    assert steel["nlsfb"] == "28.21"
    assert steel["nlsfb_material"] == "Q5"
    assert steel["etim"] == "EC001719"


def test_estimate_unknown_type_returns_error(estimator):
    result = estimator.estimate(
        building_type="nonexistent_type",
        floor_area_m2=100,
        year_built=1987,
    )
    assert "error" in result
    assert "available_keys" in result
