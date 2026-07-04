"""Project path helpers used by scripts and notebooks."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
ARTIFACTS_DIR = REPORTS_DIR / "artifacts"
MODELS_DIR = PROJECT_ROOT / "models"

RAW_TRANSACTIONS_PATH = RAW_DATA_DIR / "nova_pay_combined.csv"
CLEANED_TRANSACTIONS_PATH = PROCESSED_DATA_DIR / "cleaned_transactions.csv"
FEATURED_TRANSACTIONS_PATH = PROCESSED_DATA_DIR / "feature_engineered_transactions.csv"
BEST_ADVANCED_MODEL_PATH = MODELS_DIR / "day6" / "best_advanced_model.joblib"
