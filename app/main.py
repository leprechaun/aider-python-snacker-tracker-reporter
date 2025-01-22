from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator

from .database import get_db, init_db, Scan as DBScan, Code as DBCode

app = FastAPI()

init_db()

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

class CodeCreate(BaseModel):
    code: str = Field(..., description="Code identifier")
    name: str | None = Field(None, description="Optional name for the code")
    url: str | None = Field(None, description="Optional URL for the code")

    @field_validator('code')
    @classmethod
    def validate_ascii_code(cls, v):
        if not v.isascii():
            raise ValueError("Code must contain only ASCII characters")
        if not all(32 <= ord(char) <= 126 for char in v):
            raise ValueError("Code must contain only printable ASCII characters")
        return v

def reset_scans(db: Session):
    db.query(DBScan).delete()
    db.commit()

@app.post("/v1/scans/", status_code=201)
def create_scan(scan_data: ScanCreate, db: Session = Depends(get_db)):
    db_scan = DBScan(code=scan_data.code)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return scan_data.model_dump()

@app.get("/v1/scans/", status_code=200)
def list_scans(db: Session = Depends(get_db)):
    scans = db.query(DBScan).all()
    return [{"code": scan.code} for scan in scans]

@app.get("/v1/codes/", status_code=200)
def list_codes(db: Session = Depends(get_db)):
    return []

@app.post("/v1/codes/", status_code=201)
def create_code(code_data: CodeCreate, db: Session = Depends(get_db)):
    db_code = DBCode(code=code_data.code, name=code_data.name, url=code_data.url)
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return code_data.model_dump()
