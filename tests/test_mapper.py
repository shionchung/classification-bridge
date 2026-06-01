"""Sanity checks for classification lookup (manual_mappings.csv schema v2)."""

from __future__ import annotations

import pytest

STEEL_UNICLASS_PR = "Pr_20_93_74_16"
STEEL_ETIM = "EC001719"
STEEL_NLSFB_ELEMENT = "28.21"
STEEL_NLSFB_MATERIAL = "Q5"


def test_list_all_loads_csv(mapper):
    materials = mapper.list_all()
    assert len(materials) >= 20
    assert all("uniclass_pr" in row for row in materials)
    assert all("material_key" in row for row in materials)


def test_uniclass_lookup_known_code(mapper):
    result = mapper.uniclass_to_crosswalk(STEEL_UNICLASS_PR)
    assert result["status"] == "found"
    assert result["material_key"] == "structural_steel"
    assert result["classification"]["uniclass"]["pr"] == STEEL_UNICLASS_PR
    assert result["classification"]["etim"]["code"] == STEEL_ETIM
    assert result["classification"]["nlsfb"]["element"] == STEEL_NLSFB_ELEMENT
    assert result["classification"]["nlsfb"]["material"] == STEEL_NLSFB_MATERIAL
    assert result["review_status"] == "verified"


def test_uniclass_lookup_unknown_code(mapper):
    result = mapper.uniclass_to_crosswalk("Pr_99_99_99_99")
    assert result == {"status": "not_found", "code": "Pr_99_99_99_99"}


def test_search_by_name_finds_steel(mapper):
    results = mapper.search_by_name("steel")
    codes = {row["uniclass_pr"] for row in results}
    assert STEEL_UNICLASS_PR in codes


def test_search_by_material_key_exact(mapper):
    results = mapper.search_by_material_key("structural_steel")
    assert len(results) >= 1
    assert results[0]["material_key"] == "structural_steel"
    assert results[0]["uniclass_pr"] == STEEL_UNICLASS_PR


def test_search_by_material_key_concrete_slab(mapper):
    results = mapper.search_by_material_key("concrete_slab")
    assert len(results) == 1
    assert results[0]["material_key"] == "concrete_slab"


def test_round_trip_uniclass_matches_material_key(mapper):
    by_code = mapper.uniclass_to_crosswalk(STEEL_UNICLASS_PR)
    by_key = mapper.search_by_material_key("structural_steel")[0]
    assert by_code["classification"]["etim"]["code"] == by_key["etim_code"]
    assert by_code["classification"]["nlsfb"]["material"] == by_key.get("nlsfb_material")


def test_list_all_filter_verified(mapper):
    verified = mapper.list_all(review_status="verified")
    assert len(verified) >= 5
    assert all(r.get("review_status") == "verified" for r in verified)


def test_draft_row_may_have_empty_nlsfb_material(mapper):
    draft = mapper.list_all(review_status="needs_source")
    assert len(draft) >= 1
