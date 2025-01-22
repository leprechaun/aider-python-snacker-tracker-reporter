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

def test_create_code_rejects_non_ascii_code():
    # Test with non-ASCII characters
    non_ascii_code_data = {"code": "123456789❌"}
    response = client.post("/v1/codes/", json=non_ascii_code_data)
    assert response.status_code == 422

def test_create_code_rejects_non_printable_ascii():
    # Test with non-printable ASCII characters
    non_printable_code_data = {"code": "12345\x00\x01\x02"}
    response = client.post("/v1/codes/", json=non_printable_code_data)
    assert response.status_code == 422

def test_create_code_rejects_newline_characters():
    # Test with various newline characters
    newline_code_data_1 = {"code": "12345\n67890"}
    newline_code_data_2 = {"code": "12345\r67890"}
    newline_code_data_3 = {"code": "12345\r\n67890"}
    
    for newline_code_data in [newline_code_data_1, newline_code_data_2, newline_code_data_3]:
        response = client.post("/v1/codes/", json=newline_code_data)
        assert response.status_code == 422

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
    
    # Verify the response contains the code and url
    assert response.json()['code'] == code_data['code']
    assert response.json()['url'] == "https://example.com"
    
    # Verify the name is present and None
    assert 'name' in response.json()
    assert response.json()['name'] is None

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

def test_create_and_list_code():
    # First, create a code
    code_data = {"code": "unique_test_code"}
    create_response = client.post("/v1/codes/", json=code_data)
    assert create_response.status_code == 201

    # Then, list codes and verify the created code is returned
    list_response = client.get("/v1/codes/")
    assert list_response.status_code == 200
    
    # Check that the created code is in the list
    codes = list_response.json()
    assert any(code['code'] == code_data['code'] for code in codes)

def test_create_and_list_multiple_codes():
    # Create multiple codes
    code_data1 = {"code": "code1", "name": "Name 1", "url": "https://example1.com"}
    code_data2 = {"code": "code2", "name": "Name 2", "url": "https://example2.com"}
    
    # POST first code
    create_response1 = client.post("/v1/codes/", json=code_data1)
    assert create_response1.status_code == 201
    
    # POST second code
    create_response2 = client.post("/v1/codes/", json=code_data2)
    assert create_response2.status_code == 201

    # List codes and verify both codes are returned
    list_response = client.get("/v1/codes/")
    assert list_response.status_code == 200
    
    # Check that both codes are in the list
    codes = list_response.json()
    assert any(code['code'] == code_data1['code'] for code in codes)
    assert any(code['code'] == code_data2['code'] for code in codes)
