import os
import sys

# Add parent directory to path so Vercel can find the voidlens package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from voidlens.api import app
except Exception as e:
    # Fallback: return a minimal ASGI app that reports the error
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/{path:path}")
    async def fallback(path: str = ""):
        return {"error": "VoidLens failed to load", "detail": str(e)}
