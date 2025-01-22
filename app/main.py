from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

class ScanCreate(BaseModel):
    code: str = Field(..., description="Scan code")

    @field_validator('code')
    @classmethod
    def validate_ascii_code(cls, v):
        if not v.isascii():
            raise ValueError("Code must contain only ASCII characters")
        if not all(32 <= ord(char) <= 126 for char in v):
            raise ValueError("Code must contain only printable ASCII characters")
        return v

# In-memory storage for scans
scans = []

def reset_scans():
    global scans
    scans = []

@app.post("/v1/scans/", status_code=201)
def create_scan(scan_data: ScanCreate):
    scan = scan_data.model_dump()
    scans.append(scan)
    return scan

@app.get("/v1/scans/", status_code=200)
def list_scans():
    return scans
