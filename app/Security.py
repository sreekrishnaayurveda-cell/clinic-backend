import os
from fastapi import Header, HTTPException

# Load from Render environment variable (set in dashboard)
API_KEY = os.getenv("API_KEY")

async def require_api_key(
    x_api_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    """
    Accepts either:
    - X-API-Key: <API_KEY>
    - Authorization: Bearer <API_KEY>
    """
    if not API_KEY:
        # For safety: block if no key is set
        raise HTTPException(status_code=500, detail="Server misconfiguration: API_KEY not set")

    supplied = None
    if x_api_key:
        supplied = x_api_key.strip()
    elif authorization and authorization.lower().startswith("bearer "):
        supplied = authorization.split(" ", 1)[1].strip()

    if supplied != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
