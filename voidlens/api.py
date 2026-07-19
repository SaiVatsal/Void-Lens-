"""
VoidLens API — FastAPI REST endpoints for scan operations.

Provides POST endpoints for email and username scanning.
"""

from __future__ import annotations

from typing import Optional

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
except ImportError:
    raise ImportError("Install API extras: pip install voidlens[api]")

from voidlens import __version__
from voidlens.core.runner import scan_email, scan_username


app = FastAPI(
    title="VoidLens API",
    description="Peer into the digital void — OSINT & Digital Footprint Intelligence API",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    query: str
    categories: Optional[list[str]] = None
    modules: Optional[list[str]] = None
    concurrency: int = 100
    timeout: int = 5


class SiteResultResponse(BaseModel):
    site: str
    status: str
    url: str = ""
    category: str = ""
    reason: str = ""
    response_time: float = 0.0
    status_code: int = 0
    metadata: dict = {}


class ScanResponse(BaseModel):
    query: str
    type: str
    elapsed_seconds: float
    total: int
    found: int
    not_found: int
    unknown: int
    errors: int
    results: list[SiteResultResponse]


@app.get("/")
async def root():
    return {"name": "VoidLens", "version": __version__, "status": "operational"}


@app.post("/scan/username", response_model=ScanResponse)
async def api_scan_username(req: ScanRequest):
    """Scan a username across all registered modules."""
    try:
        result = await scan_username(
            req.query,
            categories=req.categories,
            modules=req.modules,
            concurrency=req.concurrency,
            timeout=req.timeout,
        )
        return ScanResponse(**result.to_dict())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/scan/email", response_model=ScanResponse)
async def api_scan_email(req: ScanRequest):
    """Scan an email across all registered modules."""
    try:
        result = await scan_email(
            req.query,
            categories=req.categories,
            modules=req.modules,
            concurrency=req.concurrency,
            timeout=req.timeout,
        )
        return ScanResponse(**result.to_dict())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
