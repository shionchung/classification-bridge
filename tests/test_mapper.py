"""Sanity checks for classification lookup (manual_mappings.csv)."""

from __future__ import annotations

import pytest

# Golden row: Structural steel I-beam (first verified mapping in the CSV)
STEEL_UNICLASS_PR = "Pr_20_93_74_16"
STEEL_ETIM = "EC001719"
STEEL_NLSFB = 28.21


def test_list_all_loads_csv(mapper):
    materials = mapper.list_all()
    assert len(materials) >= 20
    assert all("uniclass_pr" in row for row in materials)


def test_uniclass_lookup_known_code(mapper):
    result = mapper.uniclass_to_nlsfb(STEEL_UNICLASS_PR)
    assert result["status"] == "found"
    assert result["uniclass_pr"] == STEEL_UNICLASS_PR
    assert result["etim_code"] == STEEL_ETIM
    assert float(result["nlsfb_element"]) == STEEL_NLSFB
    assert result["material_name"] == "Structural steel I-beam"


def test_uniclass_lookup_unknown_code(mapper):
    result = mapper.uniclass_to_nlsfb("Pr_99_99_99_99")
    assert result == {"status": "not_found", "code": "Pr_99_99_99_99"}


def test_search_by_name_finds_steel(mapper):
    results = mapper.search_by_name("steel")
    codes = {row["uniclass_pr"] for row in results}
    assert STEEL_UNICLASS_PR in codes


def test_search_by_material_key_structural_steel(mapper):
    results = mapper.search_by_material_key("structural_steel")
    assert len(results) >= 1
    assert results[0]["uniclass_pr"] == STEEL_UNICLASS_PR


def test_round_trip_uniclass_matches_search(mapper):
    """Lookup by code and by name should refer to the same material."""
    by_code = mapper.uniclass_to_nlsfb(STEEL_UNICLASS_PR)
    by_key = mapper.search_by_material_key("structural_steel")[0]
    assert by_code["uniclass_pr"] == by_key["uniclass_pr"]
    assert by_code["etim_code"] == by_key["etim_code"]
    assert by_code["nlsfb_element"] == by_key["nlsfb_element"]
