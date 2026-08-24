from fastapi import APIRouter
from datetime import datetime

router = APIRouter()
_started = datetime.utcnow()

@router.get("/")
def health():
    return {"status": "ok"}

@router.get("/detailed")
def health_detailed():
    return {
        "status": "ok",
        "uptime_since": _started.isoformat() + "Z",
        "frontend": {
            "url": "http://localhost:5173/",
            "status": "unknown",
            "http_code": None,
        },
    }
