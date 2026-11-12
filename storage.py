
from pathlib import Path
import pandas as pd

COLUMNS = ["date", "type", "category", "amount", "description"]

DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_FILE = DATA_DIR / "expenses.csv"


def load_transactions():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not CSV_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)

    try:
        data = pd.read_csv(CSV_FILE)
    except (OSError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=COLUMNS)

    for column in COLUMNS:
        if column not in data.columns:
            data[column] = None

    return data[COLUMNS]


def save_transactions(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data[COLUMNS].to_csv(CSV_FILE, index=False)


BUDGET_FILE = DATA_DIR / "budget.txt"


def load_budget():
    try:
        value = float(BUDGET_FILE.read_text(encoding="utf-8").strip())
        return value if value > 0 else 10000.0
    except (OSError, ValueError):
        return 10000.0


def save_budget(amount):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BUDGET_FILE.write_text(str(amount), encoding="utf-8")
