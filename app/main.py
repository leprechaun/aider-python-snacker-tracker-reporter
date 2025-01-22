from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ScanCreate(BaseModel):
    code: str = Field(..., description="Scan code")

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
