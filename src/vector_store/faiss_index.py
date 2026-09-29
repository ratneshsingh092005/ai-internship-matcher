from pathlib import Path
import faiss
import joblib
import numpy as np


def build_index(embeddings: np.ndarray, index_path: str | Path) -> faiss.Index:
    embeddings = np.asarray(embeddings, dtype=np.float32)
    if embeddings.ndim != 2 or len(embeddings) == 0:
        raise ValueError("Embeddings must be a non-empty 2D array")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    index_path = Path(index_path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))
    return index


def load_index(index_path: str | Path) -> faiss.Index:
    path = Path(index_path)
    if not path.exists():
        raise FileNotFoundError(f"FAISS index not found: {path}")
    return faiss.read_index(str(path))


def save_metadata(metadata, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(metadata, path)


def load_metadata(path: str | Path):
    return joblib.load(path)


def search(index: faiss.Index, query_embedding: np.ndarray, top_k: int = 10):
    query = np.asarray(query_embedding, dtype=np.float32).reshape(1, -1)
    scores, indices = index.search(query, min(top_k, index.ntotal))
    return scores[0].tolist(), indices[0].tolist()
