"""Building stock CSV coverage and era bucketing."""

from __future__ import annotations

import pytest

from data import au_building_stock as stock
from data.au_building_stock import BUILDING_TYPES, ERA_ORDER, MATERIAL_INTENSITIES


def test_all_building_types_have_full_era_grid():
    """Each type should have all seven era rows in meta + intensities."""
    for building_type in BUILDING_TYPES:
        for era in ERA_ORDER:
            key = (building_type, era)
            assert key in MATERIAL_INTENSITIES, f"missing intensities for {key}"
            block = MATERIAL_INTENSITIES[key]
            assert "_confidence" in block
            assert "_source" in block
            material_keys = [k for k in block if not k.startswith("_")]
            assert len(material_keys) >= 4, f"{key} has too few materials"


def test_csv_row_count_matches_intensities_dict():
    import pandas as pd

    from data.au_building_stock import INTENSITIES_CSV

    df = pd.read_csv(INTENSITIES_CSV)
    material_rows = sum(
        len([k for k in block if not k.startswith("_")])
        for block in MATERIAL_INTENSITIES.values()
    )
    assert len(df) == material_rows


def test_reload_rereads_csv():
    before = len(MATERIAL_INTENSITIES)
    stock.reload()
    assert len(stock.MATERIAL_INTENSITIES) == before
