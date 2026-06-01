# Contributing mappings

## Adding a material row

1. Look up the same physical product in each source table (Uniclass Pr/Ss, NL-SfB, ETIM).
2. Add a row to `mappings/manual_mappings.csv`:

```csv
material_name,uniclass_pr,uniclass_ss,nlsfb_element,etim_code,confidence,notes
```

3. Set `confidence` honestly: `low` if approximate, `medium` if verified in two sources, `high` if expert-reviewed.
4. Run `pytest` — if you change a golden code in the CSV, update the constants in `tests/test_mapper.py` and `tests/test_api.py`.
5. Restart the API or Streamlit app to reload the SQLite cache.

## Priority list

Focus on high-mass materials first (structural steel, in-situ concrete, timber framing, brick, glass, insulation, plasterboard).

## Intensities (Project 3)

Edit `data/au_building_stock.py` with kg/m² values and cite the source in `_source`. Do not copy numbers without a reference.
