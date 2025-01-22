from fastapi.testclient import TestClient
from ..main import app, reset_scans

client = TestClient(app)

def setup_function():
    reset_scans()

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

def test_create_scan_rejects_non_string_code():
    invalid_scan_data = {"code": False}
    response = client.post("/v1/scans/", json=invalid_scan_data)
    assert response.status_code == 422

def test_create_scan_rejects_numeric_code():
    invalid_scan_data = {"code": 123456789}
    response = client.post("/v1/scans/", json=invalid_scan_data)
    assert response.status_code == 422

def test_create_scan_rejects_object_code():
    invalid_scan_data = {"code": {"key": "value"}}
    response = client.post("/v1/scans/", json=invalid_scan_data)
    assert response.status_code == 422

def test_get_scans_returns_empty_list():
    response = client.get("/v1/scans/")
    assert response.status_code == 200
    assert response.json() == []

import uuid

def test_create_and_list_scan():
    # First, create a scan with a random code
    scan_data = {"code": str(uuid.uuid4())}
    create_response = client.post("/v1/scans/", json=scan_data)
    assert create_response.status_code == 201

    # Then, list scans and verify the created scan is returned
    list_response = client.get("/v1/scans/")
    assert list_response.status_code == 200
    assert list_response.json() == [scan_data]

def test_create_and_list_multiple_scans():
    # Create multiple scans with random codes
    scan_data1 = {"code": str(uuid.uuid4())}
    scan_data2 = {"code": str(uuid.uuid4())}
    
    # POST first scan
    create_response1 = client.post("/v1/scans/", json=scan_data1)
    assert create_response1.status_code == 201
    
    # POST second scan
    create_response2 = client.post("/v1/scans/", json=scan_data2)
    assert create_response2.status_code == 201

    # List scans and verify both scans are returned
    list_response = client.get("/v1/scans/")
    assert list_response.status_code == 200
    
    # Sort the lists by code to compare them
    sorted_list_response = sorted(list_response.json(), key=lambda x: x['code'])
    sorted_expected = sorted([scan_data1, scan_data2], key=lambda x: x['code'])
    
    assert sorted_list_response == sorted_expected

def test_create_scan_rejects_non_ascii_code():
    # Test with non-ASCII characters
    non_ascii_scan_data = {"code": "123456789❌"}
    response = client.post("/v1/scans/", json=non_ascii_scan_data)
    assert response.status_code == 422

def test_create_scan_rejects_non_printable_ascii():
    # Test with non-printable ASCII characters
    non_printable_scan_data = {"code": "12345\x00\x01\x02"}
    response = client.post("/v1/scans/", json=non_printable_scan_data)
    assert response.status_code == 422

def test_create_scan_rejects_newline_characters():
    # Test with various newline characters
    newline_scan_data_1 = {"code": "12345\n67890"}
    newline_scan_data_2 = {"code": "12345\r67890"}
    newline_scan_data_3 = {"code": "12345\r\n67890"}
    
    for newline_scan_data in [newline_scan_data_1, newline_scan_data_2, newline_scan_data_3]:
        response = client.post("/v1/scans/", json=newline_scan_data)
        assert response.status_code == 422

def test_create_scan_accepts_url_as_code():
    # Test with various valid URLs
    url_scan_data_1 = {"code": "https://example.com"}
    url_scan_data_2 = {"code": "http://www.example.org/path?query=value"}
    url_scan_data_3 = {"code": "https://subdomain.example.co.uk/page"}
    
    for url_scan_data in [url_scan_data_1, url_scan_data_2, url_scan_data_3]:
        response = client.post("/v1/scans/", json=url_scan_data)
        assert response.status_code == 201
        assert response.json() == url_scan_data
