from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

# Strategy for generating valid ASCII printable codes
valid_code_strategy = st.text(
    alphabet=st.characters(
        blacklist_categories=('Cs', 'Cc', 'Cn'),  # Exclude surrogate and control characters
        blacklist_characters=['\n', '\r', '\t']   # Exclude newline, carriage return, tab
    ),
    min_size=1,
    max_size=50
).filter(lambda x: x.isascii() and all(32 <= ord(char) <= 126 for char in x))

@given(code=valid_code_strategy)
def test_fuzz_create_scan(code):
    """Fuzz test for creating scans with various valid codes"""
    scan_data = {"code": code}
    response = client.post("/v1/scans/", json=scan_data)
    assert response.status_code == 201
    assert response.json() == scan_data

@given(
    code=valid_code_strategy,
    name=st.one_of(st.none(), valid_code_strategy),
    url=st.one_of(st.none(), st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', '.'))))
)
def test_fuzz_create_code(code, name, url):
    """Fuzz test for creating codes with optional name and URL"""
    code_data = {"code": code}
    if name is not None:
        code_data["name"] = name
    if url is not None:
        code_data["url"] = url

    response = client.post("/v1/codes/", json=code_data)
    assert response.status_code == 201
    
    # Verify the response matches the input data
    response_json = response.json()
    assert response_json['code'] == code
    
    if name is not None:
        assert response_json['name'] == name
    else:
        assert response_json['name'] is None
    
    if url is not None:
        assert response_json['url'] == url
    else:
        assert response_json['url'] is None
