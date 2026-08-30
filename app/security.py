import secrets

from fastapi import Header, HTTPException

from app.config import get_settings


def require_internal_secret(x_internal_secret: str = Header(...)) -> None:
    settings = get_settings()
    if not secrets.compare_digest(x_internal_secret, settings.internal_api_secret):
        raise HTTPException(status_code=401, detail="Invalid or missing X-Internal-Secret header")
