from fastapi import APIRouter, UploadFile, File, Depends, Request
import numpy as np
import cv2
import asyncio

from app.security.session_guard import create_session, validate_session
from app.security.auth import verify_api_key
from app.security.rate_limit import rate_limit

from app.services.embedding import get_embedding
from app.services.similarity import search_face, check_duplicate
from app.services.video_processing import extract_frames
from app.services.vision_pipeline import run_vision_pipeline
from app.services.deepfake_check import deepfake_risk

from app.decision.decision_engine import decide
from app.db.vector_store import (
    store_face,
    get_identity_count,
    list_identities,
    reset_registry
)

from app.admin.attempt_logger import log_attempt
from app.utils.logger import log

router = APIRouter(prefix="/kyc", tags=["KYC"])


# =====================================================
# image reader
# =====================================================

async def read_image(upload: UploadFile):
    contents = await upload.read()
    arr = np.frombuffer(contents, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


# =====================================================
# session route
# =====================================================

@router.get("/session")
async def get_session(auth=Depends(verify_api_key)):
    return {"session_token": create_session()}


# =====================================================
# UNIFIED VERIFY (image + video)
# =====================================================

@router.post("/verify")
async def verify(
    request: Request,
    session_token: str,
    image: UploadFile = File(...),
    video: UploadFile = File(...),
    auth=Depends(verify_api_key)
):

    try:
        log("Unified KYC verification started")

        # --------------------
        # rate limit
        # --------------------
        client_ip = request.client.host
        if not rate_limit(client_ip):
            return {"status": "error", "reason": "Too many requests"}

        # --------------------
        # session validation
        # --------------------
        if not validate_session(session_token):
            return {"status": "error", "reason": "invalid session"}

        # =================================================
        # IMAGE → identity embedding
        # =================================================
        frame = await read_image(image)

        if frame is None:
            log_attempt({
                "type": "kyc",
                "status": "rejected",
                "reason": "invalid image"
            })
            return {"status": "rejected", "reason": "invalid image"}

        embedding = await asyncio.to_thread(
            get_embedding,
            frame
        )

        if embedding is None:
            log_attempt({
                "type": "kyc",
                "status": "rejected",
                "reason": "encoding failed"
            })
            return {"status": "rejected", "reason": "encoding failed"}

        # =================================================
        # VIDEO → liveness + deepfake checks
        # =================================================
        frames = await asyncio.to_thread(
            extract_frames,
            video
        )

        if not frames or len(frames) < 2:
            log_attempt({
                "type": "kyc",
                "status": "rejected",
                "reason": "video too short"
            })
            return {"status": "rejected", "reason": "not enough frames"}

        risk = await asyncio.to_thread(
            deepfake_risk,
            frames
        )

        if risk > 1.2:
            log_attempt({
                "type": "kyc",
                "status": "rejected",
                "reason": "deepfake suspicion"
            })
            return {"status": "rejected", "reason": "deepfake suspicion"}

        live_ok = False

        for i in range(len(frames) - 1):

            result = await asyncio.to_thread(
                run_vision_pipeline,
                frames[i],
                frames[i + 1]
            )

            if result["success"]:
                live_ok = result["liveness"]
                break

        if not live_ok:
            log_attempt({
                "type": "kyc",
                "status": "rejected",
                "reason": "liveness failed"
            })
            return {"status": "rejected", "reason": "liveness failed"}

        # =================================================
        # duplicate check
        # =================================================
        duplicate = await asyncio.to_thread(
            check_duplicate,
            embedding
        )

        decision = decide(
            live_ok,
            duplicate
        )

        if decision["status"] == "approved":
            store_face(frame, embedding)

        # =================================================
        # audit logging
        # =================================================
        log_attempt({
            "type": "kyc",
            "status": decision["status"],
            "reason": decision.get("reason", "approved"),
            "duplicate": duplicate,
            "liveness": live_ok
        })

        return decision

    except Exception as e:

        log(f"KYC verify error: {e}")

        log_attempt({
            "type": "kyc",
            "status": "error",
            "reason": "pipeline exception"
        })

        return {"status": "error", "reason": "verification failed"}


# =====================================================
# SEARCH
# =====================================================

@router.post("/search")
async def search(
    image: UploadFile = File(...),
    auth=Depends(verify_api_key)
):

    try:
        frame = await read_image(image)

        embedding = await asyncio.to_thread(
            get_embedding,
            frame
        )

        if embedding is None:
            return {"status": "rejected", "reason": "encoding failed"}

        match, score = await asyncio.to_thread(
            search_face,
            embedding
        )

        if match:
            return {
                "status": "match_found",
                "similarity_score": float(score)
            }

        return {
            "status": "no_match",
            "closest_score": float(score)
        }

    except Exception as e:
        log(f"Search error: {e}")
        return {"status": "error", "reason": "search failed"}


# =====================================================
# REGISTRY
# =====================================================

@router.get("/count")
async def identity_count(auth=Depends(verify_api_key)):
    return {"identity_count": get_identity_count()}


@router.get("/identities")
async def identities(auth=Depends(verify_api_key)):
    return {"stored_identities": list_identities()}


@router.delete("/reset")
async def reset(auth=Depends(verify_api_key)):
    reset_registry()
    return {"status": "registry cleared"}
