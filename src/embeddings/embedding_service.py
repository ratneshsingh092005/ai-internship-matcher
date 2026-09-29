from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str], normalize: bool = True) -> np.ndarray:
    if not texts:
        return np.empty((0, 384), dtype=np.float32)
    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    embeddings = np.asarray(embeddings, dtype=np.float32)
    if normalize:
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / np.clip(norms, 1e-12, None)
    return embeddings


def embedding_dimension() -> int:
    return 384
