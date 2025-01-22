from fastapi import FastAPI

app = FastAPI()

@app.post("/v1/scans/", status_code=201)
def create_scan(scan_data: dict):
    return scan_data
