from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ScanCreate(BaseModel):
    code: str = Field(..., description="Scan code")

@app.post("/v1/scans/", status_code=201)
def create_scan(scan_data: ScanCreate):
    return scan_data.model_dump()

@app.get("/v1/scans/", status_code=200)
def list_scans():
    return []
