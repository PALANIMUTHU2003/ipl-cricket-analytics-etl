from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset
DATA_PATH = BASE_DIR / "dataset" / "json files"

# Output
OUTPUT_PATH = BASE_DIR / "output"

# JSON Files
json_files = list(DATA_PATH.glob("*.json"))