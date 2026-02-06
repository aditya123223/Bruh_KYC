# backend/app/api/kyc.py

from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2

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
# helper — convert upload → OpenCV frame
# =====================================================

def read_image(upload: UploadFile):
    file_bytes = np.frombuffer(upload.file.read(), np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)


# =====================================================
# IMAGE VERIFY (2-image pipeline)
# =====================================================

@router.post("/verify")
async def verify(image1: UploadFile = File(...),
                 image2: UploadFile = File(...)):

    try:
        log("Image verification started")

        frame1 = read_image(image1)
        frame2 = read_image(image2)

        if frame1 is None or frame2 is None:
            return {"status": "rejected", "reason": "invalid image"}

        pipeline_result = run_vision_pipeline(frame1, frame2)

        if not pipeline_result["success"]:
            return {
                "status": "rejected",
                "reason": pipeline_result["error"]
            }

        embedding = pipeline_result["embedding"]

        duplicate = check_duplicate(embedding)

        decision = decide(
            pipeline_result["liveness"],
            duplicate
        )

        if decision["status"] == "approved":
            store_face(frame2, embedding)

        return decision

    except Exception as e:
        log(f"Verify error: {e}")
        return {"status": "error", "reason": "verification failed"}


# =====================================================
# SEARCH IDENTITY
# =====================================================

@router.post("/search")
async def search(image: UploadFile = File(...)):

    try:
        log("Identity search started")

        frame = read_image(image)

        if frame is None:
            return {"status": "error", "reason": "invalid image"}

        embedding = get_embedding(frame)

        if embedding is None:
            return {
                "status": "rejected",
                "reason": "encoding failed"
            }

        match, score = search_face(embedding)

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
# VIDEO VERIFY (deepfake → liveness → duplicate)
# =====================================================

@router.post("/verify-video")
async def verify_video(video: UploadFile = File(...)):

    try:
        log("Video verification started")

        frames = extract_frames(video)

        if len(frames) < 2:
            return {
                "status": "rejected",
                "reason": "not enough frames"
            }

        # -------------------------
        # deepfake heuristic
        # -------------------------
        risk = deepfake_risk(frames)

        log(f"Deepfake risk score: {risk}")

        if risk > 1.2:
            return {
                "status": "rejected",
                "reason": "deepfake suspicion"
            }

        # -------------------------
        # liveness + pipeline
        # -------------------------
        pipeline_result = None
        selected_frame = None

        for i in range(len(frames) - 1):

            test = run_vision_pipeline(frames[i], frames[i + 1])

            if test["success"]:
                pipeline_result = test
                selected_frame = frames[i + 1]
                break

        if pipeline_result is None:
            return {
                "status": "rejected",
                "reason": "liveness failed"
            }

        embedding = pipeline_result["embedding"]

        duplicate = check_duplicate(embedding)

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
# REGISTRY ENDPOINTS
# =====================================================

@router.get("/count")
async def identity_count():
    return {"identity_count": get_identity_count()}


@router.get("/identities")
async def identities():
    return {"stored_identities": list_identities()}


@router.delete("/reset")
async def reset():
    reset_registry()
    return {"status": "registry cleared"}