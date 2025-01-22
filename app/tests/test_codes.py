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
    
    # Check that the response contains the code and optionally name
    assert response.json()['code'] == code_data['code']
    assert 'name' in response.json()
    assert response.json()['name'] is None

def test_create_code_returns_same_data_structure():
    code_data = {"code": "123456789"}
    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    
    # Check that the response has the same keys and types as the request
    assert isinstance(response.json(), dict)
    assert 'code' in response.json()
    assert isinstance(response.json()['code'], str)
    assert 'name' in response.json()
    assert response.json()['name'] is None

def test_create_code_with_optional_name():
    code_data = {"code": "123456789", "name": "Test Code"}
    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    
    # Verify the response contains the code and name
    assert response.json()['code'] == code_data['code']
    assert response.json()['name'] == "Test Code"
    
    # Verify the url is present and None
    assert 'url' in response.json()
    assert response.json()['url'] is None

def test_create_code_with_optional_url():
    code_data = {"code": "123456789", "url": "https://example.com"}
    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    assert response.json() == code_data
    
    # Verify the optional url is correctly handled
    assert 'url' in response.json()
    assert response.json()['url'] == "https://example.com"

def test_create_code_with_name_and_url():
    code_data = {"code": "123456789", "name": "Test Code", "url": "https://example.com"}
    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    assert response.json() == code_data
    
    # Verify both optional name and url are correctly handled
    assert 'name' in response.json()
    assert response.json()['name'] == "Test Code"
    assert 'url' in response.json()
    assert response.json()['url'] == "https://example.com"
