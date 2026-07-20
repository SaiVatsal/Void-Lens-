import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VoidLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"name": "VoidLens", "version": "1.0.0", "status": "operational"}


@app.get("/api")
async def api_root():
    return {"name": "VoidLens", "version": "1.0.0", "status": "operational"}


@app.post("/api/scan/username")
async def api_scan_username(req: dict):
    try:
        from voidlens.core.runner import scan_username
        result = await scan_username(req.get("query", ""))
        return result.to_dict()
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/scan/email")
async def api_scan_email(req: dict):
    try:
        from voidlens.core.runner import scan_email
        result = await scan_email(req.get("query", ""))
        return result.to_dict()
    except Exception as e:
        return {"error": str(e)}
