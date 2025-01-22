from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_scan_requires_body():
    response = client.post("/v1/scans/")
    assert response.status_code == 422

def test_create_scan_returns_request_body():
    scan_data = {"code": "123456789"}
    response = client.post("/v1/scans/", json=scan_data)
    assert response.status_code == 201
    assert response.json() == scan_data

def test_create_scan_rejects_invalid_data_structure():
    invalid_scan_data = {"invalid_key": "123456789"}
    response = client.post("/v1/scans/", json=invalid_scan_data)
    assert response.status_code == 422

def test_create_scan_rejects_empty_object():
    empty_scan_data = {}
    response = client.post("/v1/scans/", json=empty_scan_data)
    assert response.status_code == 422
