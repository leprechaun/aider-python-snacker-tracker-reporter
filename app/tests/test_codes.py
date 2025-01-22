from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_get_codes_returns_empty_list():
    response = client.get("/v1/codes/")
    assert response.status_code == 200
    assert response.json() == []
