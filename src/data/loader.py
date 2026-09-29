from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "job_id", "title", "company", "location", "description", "skills",
    "experience_required", "employment_type", "salary", "remote", "application_url"
]


def load_internships(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path).fillna("")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")
    return df
