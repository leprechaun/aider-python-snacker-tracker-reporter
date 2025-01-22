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

def test_create_code_returns_same_data_structure():
    code_data = {"code": "123456789"}
    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    
    # Check that the response has the same keys and types as the request
    assert isinstance(response.json(), dict)
    assert list(response.json().keys()) == list(code_data.keys())
    assert isinstance(response.json()['code'], str)

def test_create_code_with_optional_name():
    code_data = {"code": "123456789", "name": "Test Code"}
    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    assert response.json() == code_data
    
    # Verify the optional name is correctly handled
    assert 'name' in response.json()
    assert response.json()['name'] == "Test Code"
