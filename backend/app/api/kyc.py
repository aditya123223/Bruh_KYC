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

from app.utils.logger import log

router = APIRouter(prefix="/kyc", tags=["KYC"])


# =====================================================
# async image reader
# =====================================================

async def read_image(upload: UploadFile):
    contents = await upload.read()
    arr = np.frombuffer(contents, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


# =====================================================
# SESSION ROUTE
# =====================================================

@router.get("/session")
async def get_session(auth=Depends(verify_api_key)):
    return {"session_token": create_session()}


# =====================================================
# IMAGE VERIFY
# =====================================================

@router.post("/verify")
async def verify(
    request: Request,
    session_token: str,
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    auth=Depends(verify_api_key)
):

    try:
        log("Image verification started")

        # ---- rate limit ----
        client_ip = request.client.host

        if not rate_limit(client_ip):
            return {
                "status": "error",
                "reason": "Too many requests — slow down"
            }

        # ---- session validation ----
        if not validate_session(session_token):
            return {
                "status": "error",
                "reason": "invalid or expired session"
            }

        # ---- read images ----
        frame1 = await read_image(image1)
        frame2 = await read_image(image2)

        if frame1 is None or frame2 is None:
            return {"status": "rejected", "reason": "invalid image"}

        # ---- pipeline ----
        pipeline_result = await asyncio.to_thread(
            run_vision_pipeline,
            frame1,
            frame2
        )

        if not pipeline_result["success"]:
            return {
                "status": "rejected",
                "reason": pipeline_result["error"]
            }

        embedding = pipeline_result.get("embedding")

        if embedding is None:
            return {"status": "error", "reason": "embedding failure"}

        # ---- duplicate check ----
        duplicate = await asyncio.to_thread(
            check_duplicate,
            embedding
        )

        decision = decide(
            pipeline_result["liveness"],
            duplicate
        )

        # ---- storage ----
        if decision["status"] == "approved":
            store_face(frame2, embedding)

        return decision

    except Exception as e:
        log(f"Verify error: {e}")
        return {
            "status": "error",
            "reason": "verification failed"
        }


# =====================================================
# SEARCH
# =====================================================

@router.post("/search")
async def search(
    image: UploadFile = File(...),
    auth=Depends(verify_api_key)
):

    try:
        log("Identity search started")

        frame = await read_image(image)

        if frame is None:
            return {"status": "error", "reason": "invalid image"}

        embedding = await asyncio.to_thread(get_embedding, frame)

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
# VIDEO VERIFY
# =====================================================

@router.post("/verify-video")
async def verify_video(
    request: Request,
    video: UploadFile = File(...),
    auth=Depends(verify_api_key)
):

    try:
        log("Video verification started")

        # ---- rate limit ----
        client_ip = request.client.host

        if not rate_limit(client_ip):
            return {
                "status": "error",
                "reason": "Too many requests — slow down"
            }

        # ---- extract frames ----
        frames = await asyncio.to_thread(extract_frames, video)

        if not frames or len(frames) < 2:
            return {"status": "rejected", "reason": "not enough frames"}

        # ---- deepfake check ----
        risk = await asyncio.to_thread(deepfake_risk, frames)

        if risk > 1.2:
            return {"status": "rejected", "reason": "deepfake suspicion"}

        pipeline_result = None
        selected_frame = None

        for i in range(len(frames) - 1):

            test = await asyncio.to_thread(
                run_vision_pipeline,
                frames[i],
                frames[i + 1]
            )

            if test["success"]:
                pipeline_result = test
                selected_frame = frames[i + 1]
                break

        if pipeline_result is None:
            return {"status": "rejected", "reason": "liveness failed"}

        embedding = pipeline_result.get("embedding")

        if embedding is None:
            return {"status": "error", "reason": "embedding failure"}

        duplicate = await asyncio.to_thread(
            check_duplicate,
            embedding
        )

        decision = decide(
            pipeline_result["liveness"],
            duplicate
        )

        if decision["status"] == "approved":
            store_face(selected_frame, embedding)

        return decision

    except Exception as e:
        log(f"Video error: {e}")
        return {"status": "error", "reason": "video verification failed"}


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
