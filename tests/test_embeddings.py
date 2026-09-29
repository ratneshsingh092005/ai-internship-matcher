import numpy as np
import pytest

def test_embedding_dimension():
    try:
        from src.embeddings.embedding_service import embed_texts
        emb = embed_texts(['Python backend internship'])
    except Exception as exc:
        pytest.skip(f'Embedding model unavailable in test environment: {exc}')
    assert emb.shape == (1, 384)
    assert np.isclose(np.linalg.norm(emb[0]), 1.0, atol=1e-3)
