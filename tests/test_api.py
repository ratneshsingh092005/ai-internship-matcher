import pytest
pytest.importorskip("fastapi")
pytest.importorskip("faiss")
pytest.importorskip("sentence_transformers")
from fastapi.testclient import TestClient
from app.main import app

def test_health_route():
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200

def test_top_k_validation():
    client = TestClient(app)
    response = client.post('/match-internships', json={'resume_text':'Python backend developer with Docker and SQL experience.', 'top_k':0})
    assert response.status_code == 422
