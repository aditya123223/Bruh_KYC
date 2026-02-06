import os
from fastapi import Header, HTTPException

# Load API key from environment
API_KEY = os.getenv("API_KEY", "hackathon-demo-key")


def verify_api_key(x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
