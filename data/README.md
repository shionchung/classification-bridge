# Data files

## Building stock intensities (Project 3)

Editable in Excel or any spreadsheet — no Python required:

| File | Columns |
|------|---------|
| `au_material_intensities.csv` | `building_type`, `era`, `material_key`, `kg_per_m2` |
| `au_building_stock_meta.csv` | `building_type`, `era`, `confidence`, `source` |

`au_building_stock.py` loads these at import time. Building types: `commercial_office`, `residential_detached`, `residential_apartment`, `education`, `industrial_warehouse`. Eras split around **1980** and **2005**.

---

## Classification source files (download manually)

Place downloaded spreadsheets here. Large vendor files are gitignored.

| File | Source |
|------|--------|
| `uniclass_pr.xlsx` | [NBS Uniclass](https://www.thenbs.com/uniclass) — Products (Pr) |
| `uniclass_ss.xlsx` | NBS Uniclass — Systems (Ss) |
| `uniclass_ef.xlsx` | NBS Uniclass — Elements/Functions (EF) |
| `nlsfb.xlsx` | NL-SfB 2005 — [BIM Loket](https://www.bimloket.nl/) / stabu.nl |
| `etim.xlsx` | [ETIM International](https://www.etim-international.com/) (free registration) |
| `omniclass.xlsx` | [CSI OmniClass](https://www.csinet.org/omniclass) (optional) |

After downloading, run:

```bash
python -m src.loader --explore
```
