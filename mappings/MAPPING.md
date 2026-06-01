# Classification mapping ontology

This document defines what each code column in [`manual_mappings.csv`](manual_mappings.csv) means. Read this before adding rows.

## Three different questions

| System | Table / level | Answers | Use in passport |
|--------|---------------|---------|-----------------|
| **Uniclass Pr** | Products | What product is installed? | AU BIM exports, procurement |
| **Uniclass Ss** | Systems | Which system context? | Optional context; not a substitute for NL-SfB Table 1 |
| **NL-SfB Table 1** | Elements (`nlsfb_element`) | Where / what building part? | Madaster-style element location |
| **NL-SfB Table 3** | Materials (`nlsfb_material`) | What material type? | Circularity, urban mining, EPD grouping |
| **ETIM** | Product classes | Supplier catalogue category? | EPD lookup, procurement |

**Do not collapse these into one field.** `28.21` (Table 1) means “load-bearing steel structure of the building”, not “steel” as a material.

## Dual NL-SfB rule

Every curated row should populate **both** where possible:

- `nlsfb_element` — NL-SfB **Table 1** (element by position/function). Madaster-oriented.
- `nlsfb_material` — NL-SfB **Table 3** (material type, e.g. `Q5` steel/iron). Circularity-oriented.

If Table 3 is unknown, leave `nlsfb_material` empty and set `review_status=needs_source`.

## Edition pins

| Column | Default |
|--------|---------|
| `uniclass_edition` | `2015` (AU practice; note 2022 separately when adopted) |
| `nlsfb_edition` | `2005` |
| `etim_version` | `9` |

When a standard updates, change the edition column — do not silently overwrite codes.

## Review gates

| `review_status` | Meaning |
|-----------------|---------|
| `draft` | Placeholder or single-source; OK for demos |
| `needs_source` | Missing Table 3 or unverified ETIM |
| `verified` | Two independent sources noted in `mapping_notes`; safe for publications |

Only cite `verified` rows in reports or policy submissions.

## Core materials (map these first)

Mass-dominated Australian stock — target ~20 rows before expanding to 50:

1. Structural steel  
2. Reinforced concrete — **slab**, **column**, **beam** (separate rows; different recycling paths)  
3. Precast concrete  
4. Concrete slab (ground bearing)  
5. Brick / blockwork  
6. Structural timber (softwood framing)  
7. Engineered timber (LVL / glulam)  
8. Float glass  
9. Aluminium extrusions  
10. Aluminium cladding  
11. Plasterboard  
12. Mineral wool insulation  
13. EPS insulation  
14. Membrane roofing  
15. Galvanised steel (roofing / cladding)  
16. Copper  
17. Portland cement (bulk)  
18. Ceramic tile  
19. Carpet  
20. Vinyl flooring  

## Curation workflow

1. Download source tables — see [`data/README.md`](../data/README.md).  
2. Optional: run `python scripts/suggest_etim_matches.py` for ETIM **candidates** (never auto-commit).  
3. Curate in Google Sheet using `scripts/export_mapping_template.py` output; export CSV.
4. Replace `manual_mappings.csv`; run `pytest`.
5. Per row: Uniclass Pr (NBS) → ETIM (confirm) → NL-SfB Table 3 → NL-SfB Table 1.

Use `python scripts/suggest_etim_matches.py` for **candidates only** — fuzzy scores live in `mappings/etim_candidates.csv`, not in `manual_mappings.csv` (verified rows must not imply algorithmic mapping).

Git CSV is the **only** canonical store.

## Passport output (`0.2-AU`)

Each material row includes nested `classification`:

```json
"classification": {
  "uniclass": { "pr": "...", "ss": "...", "edition": "2015" },
  "nlsfb": { "element": "28.21", "material": "Q5", "edition": "2005" },
  "etim": { "code": "EC001719", "version": "9" }
}
```

Legacy flat `nlsfb` / `etim` keys remain when `legacy_flat_codes=true` on the estimator.
