from fastapi.testclient import TestClient
from snacker_tracker_reporter.main import app

client = TestClient(app)

def test_create_scan():
    response = client.post("/v1/scans/")
    assert response.status_code == 201
