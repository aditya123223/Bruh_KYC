from fastapi import APIRouter, Depends
import json
import os

from app.security.auth import verify_api_key

router = APIRouter(prefix="/admin", tags=["Admin"])

LOG_FILE = "attempt_log.json"


@router.get("/attempts")
async def get_attempts(auth=Depends(verify_api_key)):

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        return json.load(f)


@router.get("/stats")
async def get_stats(auth=Depends(verify_api_key)):

    if not os.path.exists(LOG_FILE):
        return {"total": 0}

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    approved = sum(1 for l in logs if l["status"] == "approved")
    rejected = sum(1 for l in logs if l["status"] == "rejected")

    return {
        "total_attempts": len(logs),
        "approved": approved,
        "rejected": rejected
    }
