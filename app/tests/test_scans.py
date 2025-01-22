from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_scan():
    response = client.post("/v1/scans/")
    assert response.status_code == 201

def test_create_scan_returns_request_body():
    scan_data = {"code": "123456789"}
    response = client.post("/v1/scans/", json=scan_data)
    assert response.status_code == 201
    assert response.json() == scan_data
