from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MAPPINGS_DIR = ROOT / "mappings"
MANUAL_MAPPINGS_CSV = MAPPINGS_DIR / "manual_mappings.csv"
DEFAULT_DB = ROOT / "mappings.db"
