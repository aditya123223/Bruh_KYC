from fastapi import APIRouter, UploadFile, File, Form, Depends, Request
import numpy as np
import cv2
import asyncio
import tempfile
import os

from app.security.session_guard import create_session, validate_session
from app.security.auth import verify_api_key
from app.security.rate_limit import rate_limit

from app.services.embedding import get_embedding
from app.services.similarity import (
    search_face,
    check_duplicate,
    verify_identity_match
)
from app.services.video_processing import extract_frames
from app.services.active_liveness import active_liveness_from_video

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
# VERIFY — selfie + video pipeline
# =====================================================

@router.post("/verify")
async def verify(
    request: Request,
    session_token: str = Form(...),
    image: UploadFile = File(...),
    video: UploadFile = File(...),
    auth=Depends(verify_api_key)
):
    try:
        log("[KYC] Unified verification started")

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
        # SELFIE → embedding
        # =================================================
        selfie_frame = await read_image(image)

        if selfie_frame is None:
            log_attempt({"type": "kyc", "status": "rejected", "reason": "invalid image"})
            return {"status": "rejected", "reason": "invalid image"}

        selfie_embedding = await asyncio.to_thread(get_embedding, selfie_frame)

        if selfie_embedding is None:
            log_attempt({"type": "kyc", "status": "rejected", "reason": "encoding failed"})
            return {"status": "rejected", "reason": "encoding failed"}

        # =================================================
        # SAVE VIDEO ONCE
        # =================================================
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            contents = await video.read()
            tmp.write(contents)
            video_path = tmp.name

        # =================================================
        # ACTIVE LIVENESS
        # =================================================
        liveness_result = await asyncio.to_thread(active_liveness_from_video, video_path)
        print("Active liveness result:", liveness_result)

        if not liveness_result.get("is_live", False):
            os.remove(video_path)
            log_attempt({
                "type": "kyc",
                "status": "rejected",
                "reason": "liveness failed",
                "metrics": liveness_result
            })
            return {"status": "rejected", "reason": "liveness failed"}

        # =================================================
        # FRAME EXTRACTION
        # =================================================
        frames = await asyncio.to_thread(extract_frames, video_path)
        os.remove(video_path)

        if not frames:
            return {"status": "rejected", "reason": "video processing failed"}

        # =================================================
        # IDENTITY MATCH — multi-frame averaging
        # =================================================
        scores = []
        for frame in frames:
            video_emb = await asyncio.to_thread(get_embedding, frame)
            if video_emb is None:
                continue

            match, score = await asyncio.to_thread(
                verify_identity_match,
                selfie_embedding,
                video_emb
            )
            print("Identity score:", score)
            scores.append(score)

        if not scores:
            return {"status": "rejected", "reason": "identity check failed"}

        avg_score = sum(scores) / len(scores)
        print("Average identity score:", avg_score)

        IDENTITY_THRESHOLD = 0.70
        if avg_score < IDENTITY_THRESHOLD:
            log_attempt({
                "type": "kyc",
                "status": "rejected",
                "reason": "identity mismatch",
                "similarity": float(avg_score)
            })
            return {
                "status": "rejected",
                "reason": "identity mismatch",
                "similarity": float(avg_score)
            }

        # =================================================
        # DUPLICATE CHECK
        # =================================================
        duplicate = await asyncio.to_thread(check_duplicate, selfie_embedding)
        decision = decide(True, duplicate)

        if decision["status"] == "approved":
            store_face(selfie_frame, selfie_embedding)

        decision["active_liveness"] = liveness_result

        # =================================================
        # AUDIT LOG
        # =================================================
        log_attempt({
            "type": "kyc",
            "status": decision["status"],
            "reason": decision.get("reason", "approved"),
            "duplicate": duplicate,
            "liveness": True,
            "similarity": float(avg_score)
        })

        return decision

    except Exception as e:
        print("KYC PIPELINE ERROR:", e)
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
        embedding = await asyncio.to_thread(get_embedding, frame)

        if embedding is None:
            return {"status": "rejected", "reason": "encoding failed"}

        match, score = await asyncio.to_thread(search_face, embedding)

        if match:
            return {"status": "match_found", "similarity_score": float(score)}

        return {"status": "no_match", "closest_score": float(score)}

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

