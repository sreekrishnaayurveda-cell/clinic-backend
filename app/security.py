import os
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY")

async def require_api_key(
    x_api_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API_KEY not set")

    supplied = None
    if x_api_key:
        supplied = x_api_key.strip()
    elif authorization and authorization.lower().startswith("bearer "):
        supplied = authorization.split(" ", 1)[1].strip()

    if supplied != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
