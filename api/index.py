import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="VoidLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
@app.get("/api/")
async def api_root():
    return {"name": "VoidLens", "version": "1.0.0", "status": "operational"}


@app.post("/api/scan/username")
async def api_scan_username(request: Request):
    try:
        body = await request.json()
        query = body.get("query", "")
        if not query:
            return JSONResponse({"error": "query is required"}, status_code=400)
        from voidlens.core.runner import scan_username
        result = await scan_username(query)
        return result.to_dict()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=200)


@app.post("/api/scan/email")
async def api_scan_email(request: Request):
    try:
        body = await request.json()
        query = body.get("query", "")
        if not query:
            return JSONResponse({"error": "query is required"}, status_code=400)
        from voidlens.core.runner import scan_email
        result = await scan_email(query)
        return result.to_dict()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=200)
