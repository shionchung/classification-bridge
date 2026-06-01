# Data files

## Building stock intensities (Project 3)

Editable in Excel or any spreadsheet — no Python required:

| File | Columns |
|------|---------|
| `au_material_intensities.csv` | `building_type`, `era`, `material_key`, `kg_per_m2` |
| `au_building_stock_meta.csv` | `building_type`, `era`, `confidence`, `source` |

`au_building_stock.py` loads these at import time. Building types: `commercial_office`, `residential_detached`, `residential_apartment`, `education`, `industrial_warehouse`. Eras split around **1980** and **2005**.

---

## Classification source files

**One-command download** (Uniclass, NL-SfB, ETIM — ~15 MB total, gitignored):

```powershell
python scripts/download_source_data.py
```

Status table: [`DOWNLOAD_STATUS.md`](DOWNLOAD_STATUS.md). Large vendor files stay local only.

| File | Source |
|------|--------|
| `uniclass_pr.xlsx` | [NBS Uniclass](https://www.thenbs.com/uniclass) — Products (Pr) |
| `uniclass_ss.xlsx` | NBS Uniclass — Systems (Ss) |
| `uniclass_ef.xlsx` | NBS Uniclass — Elements/Functions (EF) |
| `nlsfb_table1.xlsx` | NL-SfB **Table 1** — elements (position/function) → `nlsfb_element` in mappings |
| `nlsfb_table3.xlsx` | NL-SfB **Table 3** — materials (e.g. Q5 steel) → `nlsfb_material` in mappings |
| `nlsfb.xlsx` | Optional combined export if Table 1+3 not split |
| `etim.xlsx` | [ETIM International](https://www.etim-international.com/) — ETIM 9 (free registration) |
| `omniclass.xlsx` | [CSI OmniClass](https://www.csinet.org/omniclass) (optional) |

After downloading, run:

```bash
python -m src.loader --explore
python -m src.loader --table nlsfb1   # Table 1 only
python -m src.loader --table nlsfb3   # Table 3 only
```

See [`mappings/MAPPING.md`](../mappings/MAPPING.md) for how Table 1 and Table 3 differ.
