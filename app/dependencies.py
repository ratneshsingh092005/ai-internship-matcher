from pathlib import Path
from functools import lru_cache
from src.vector_store.faiss_index import load_index, load_metadata
from .services.matching_service import MatchingService

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "internships.csv"
INDEX = ROOT / "models" / "internship_index.faiss"
METADATA = ROOT / "models" / "internship_metadata.joblib"


@lru_cache(maxsize=1)
def get_matching_service() -> MatchingService:
    return MatchingService(DATASET, load_index(INDEX), load_metadata(METADATA))
