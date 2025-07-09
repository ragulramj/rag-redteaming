from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_rag_missing_query():
    response = client.post('/rag', json={})
    assert response.status_code == 422
