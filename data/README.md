# Classification source files (download manually)

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
