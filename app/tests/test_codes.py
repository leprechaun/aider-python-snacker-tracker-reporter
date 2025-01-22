from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_get_codes_returns_empty_list():
    response = client.get("/v1/codes/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_code_returns_request_body():
    code_data = {"code": "123456789"}
    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    assert response.json() == code_data
