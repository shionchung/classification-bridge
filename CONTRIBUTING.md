# Contributing mappings

Read [`mappings/MAPPING.md`](mappings/MAPPING.md) first — it explains Uniclass Pr vs NL-SfB Table 1 vs Table 3 vs ETIM.

## Adding a material row

1. Look up the product in Uniclass Pr (NBS), ETIM 9, NL-SfB Table 1 (element), and NL-SfB Table 3 (material).
2. Add a row to [`mappings/manual_mappings.csv`](mappings/manual_mappings.csv) (schema v2):

```csv
material_key,material_name,uniclass_pr,uniclass_ss,uniclass_edition,nlsfb_element,nlsfb_material,nlsfb_edition,etim_code,etim_version,confidence,review_status,mapping_notes,fuzzy_match_score
```

3. Set `review_status=verified` only when two independent sources are cited in `mapping_notes`.
4. Run `pytest` — update golden constants in `tests/test_mapper.py` if codes change.
5. Restart the API or Streamlit app to reload the SQLite cache.

### Google Sheet workflow

```powershell
python scripts/export_mapping_template.py
```

Import `mappings/mapping_curation_template.csv` into a Sheet, curate, export CSV, replace `manual_mappings.csv`. Git CSV remains canonical.

### ETIM fuzzy candidates (assist only)

```powershell
pip install -r requirements-dev.txt
python scripts/suggest_etim_matches.py
```

Review `mappings/etim_candidates.csv` — never auto-merge into `manual_mappings.csv`.

## Priority list

See **Core materials** in `MAPPING.md`. Map mass-dominated materials first; split reinforced concrete into slab / column / beam rows.

## Intensities (Project 3)

| File | Purpose |
|------|---------|
| `data/au_material_intensities.csv` | `building_type`, `era`, `material_key`, `kg_per_m2` |
| `data/au_building_stock_meta.csv` | `building_type`, `era`, `confidence`, `source` |

`material_key` must match a row in `manual_mappings.csv`. Run `pytest` after edits.
