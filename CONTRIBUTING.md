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

Edit the CSV files (no Python required):

| File | Purpose |
|------|---------|
| `data/au_material_intensities.csv` | `building_type`, `era`, `material_key`, `kg_per_m2` |
| `data/au_building_stock_meta.csv` | `building_type`, `era`, `confidence`, `source` |

Add one row per material in the intensities file. Set `confidence` and `source` once per type × era in the meta file. Era buckets: `pre_1960`, `1960_1979`, `1980_1989`, `1990_1999`, `2000_2004`, `2005_2014`, `2015_present`.

Do not copy kg/m² numbers without a reference. Run `pytest` after edits.
