# classification-bridge

**Open AU ↔ EU classification mapping + material passport estimates for buildings without BIM.**

Most Australian buildings have no BIM model — only drawings, photos, and basic metadata. EU material passport platforms (Madaster, Circularise) expect **NL-SfB** and **ETIM** codes, while Australian BIM uses **Uniclass 2015**. This repo provides:

1. **Project 4 — Classification Bridge** — hand-curated crosswalk (Uniclass → NL-SfB → ETIM) with a FastAPI lookup service  
2. **Project 3 — Material Passport Estimator** — kg/m² intensities by building type and era → estimated passport JSON with embedded classification codes  

> **Status:** Early research prototype. Mapping codes and material intensities include placeholders marked `low` confidence until verified against source tables and AHURI / Stephan & Crawford literature.

---

## Why it matters

- Enables cross-border material data exchange (Australian Uniclass exports readable by EU platforms).  
- Supports urban-mining / circularity screening for **existing** Australian stock before any material-passport mandate.  
- Documents uncertainty explicitly (`confidence` per mapping, `_source` per intensity block).

---

## Quick start

**Requirements:** Python 3.11+ ([python.org](https://www.python.org/downloads/)) — enable “Add python.exe to PATH” on Windows.

```powershell
git clone https://github.com/YOUR_USERNAME/classification-bridge.git
cd classification-bridge
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Web UI (material passport)

```powershell
streamlit run app.py
```

Enter building type, gross floor area (m²), and year built → download `material_passport.json`.

### REST API (classification lookup)

```powershell
uvicorn src.api:app --reload
```

| Endpoint | Description |
|----------|-------------|
| `GET /map/uniclass/{code}` | Map a Uniclass Pr code to NL-SfB + ETIM |
| `GET /search/{query}` | Search materials by name |
| `GET /materials` | List all mapped materials |
| `GET /health` | Health check |

Example: `http://127.0.0.1:8000/map/uniclass/Pr_20_93_74_16`

### CLI example

```powershell
python -m src.material_estimator
```

---

## Source data downloads

Place Excel exports in `data/` (see [data/README.md](data/README.md)):

| File | Source |
|------|--------|
| `uniclass_pr.xlsx`, `uniclass_ss.xlsx` | [NBS Uniclass](https://www.thenbs.com/uniclass) |
| `nlsfb.xlsx` | NL-SfB 2005 (BIM Loket / stabu.nl) |
| `etim.xlsx` | [ETIM International](https://www.etim-international.com/) |

Explore loaded tables:

```powershell
python -m src.loader --explore
```

---

## Project structure

```
classification-bridge/
├── app.py                      # Streamlit UI
├── mappings/manual_mappings.csv
├── data/
│   ├── au_building_stock.py    # kg/m² by (type, era)
│   └── README.md
└── src/
    ├── api.py                  # FastAPI
    ├── mapper.py               # SQLite-backed lookup
    ├── loader.py               # Excel explorer
    └── material_estimator.py
```

---

## Example output

```json
{
  "building_type": "commercial_office",
  "floor_area_m2": 3500,
  "year_built": 1987,
  "era": "1980_1999",
  "confidence": "low",
  "materials": [
    {
      "material": "structural_steel",
      "estimated_kg": 182000,
      "uniclass_pr": "Pr_20_93_74_16",
      "nlsfb": "28.21",
      "etim": "EC001719"
    }
  ],
  "passport_format_version": "0.1-AU"
}
```

---

## Roadmap

| Phase | Goal |
|-------|------|
| Month 1 | 50 verified material mappings, public GitHub repo |
| Month 2 | Literature-backed intensities (3 types × 3 eras), stable JSON schema |
| Month 3 | Streamlit polish, Madaster field alignment, contributor docs |

---

## Research references

- [AHURI Final Report 402](https://www.ahuri.edu.au/) — *Building materials in a circular economy*  
- Stephan & Crawford (Uni Melbourne) — material stock analysis (kg/m²)  
- [Madaster — material passport](https://docs.madaster.com/)  
- [Ellen MacArthur — Circularity Indicators](https://ellenmacarthurfoundation.org/)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests welcome for verified mapping rows (include source notes and confidence).

---

## License

[MIT](LICENSE)
