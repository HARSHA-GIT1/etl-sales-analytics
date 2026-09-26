from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Source files
SALES_DATA_FILE = RAW_DATA_DIR / "samplesuperstore.csv"

# Database
DATABASE_FILE = PROCESSED_DATA_DIR / "sales.db"

# External API
FRANKFURTER_BASE_URL = "https://api.frankfurter.dev/v1"