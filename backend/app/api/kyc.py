# backend/app/api/kyc.py

from app.services.active_liveness import active_liveness_from_video
import tempfile
import os

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
        log("Layered video verification started")

        # --------------------------------
        # save temp video for active liveness
        # --------------------------------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(video.file.read())
            video_path = tmp.name

        # --------------------------------
        # frame extraction (FIXED)
        # --------------------------------
        frames = extract_frames(video_path)

        if len(frames) < 2:
            os.remove(video_path)
            return {
                "status": "rejected",
                "reason": "not enough frames"
            }

        # --------------------------------
        # 1️⃣ PASSIVE liveness gate
        # --------------------------------
        passive_result = None
        selected_frame = None

        for i in range(len(frames) - 1):
            test = run_vision_pipeline(frames[i], frames[i + 1])
            if test["success"]:
                passive_result = test
                selected_frame = frames[i + 1]
                break

        if passive_result is None:
            os.remove(video_path)
            return {
                "status": "rejected",
                "reason": "passive liveness failed"
            }

        # --------------------------------
        # 2️⃣ ACTIVE behavioral liveness
        # --------------------------------
        active = active_liveness_from_video(video_path)

        os.remove(video_path)

        if not active.get("is_live", False):
            return {
                "status": "rejected",
                "reason": "active liveness failed",
                "confidence": active.get("confidence", 0)
            }

        # --------------------------------
        # 3️⃣ deepfake heuristic
        # --------------------------------
        risk = deepfake_risk(frames)

        if risk > 1.2:   # demo-safe threshold
            return {
                "status": "rejected",
                "reason": "deepfake suspicion"
            }

        # --------------------------------
        # 4️⃣ identity embedding
        # --------------------------------
        embedding = passive_result["embedding"]

        duplicate = check_duplicate(embedding)

        decision = decide(
            passive_result["liveness"],
            duplicate
        )

        if decision["status"] == "approved":
            store_face(selected_frame, embedding)

        # attach liveness metrics for demo
        decision["active_confidence"] = active["confidence"]

        return decision

    except Exception as e:
        log(f"Video pipeline error: {str(e)}")
        return {
            "status": "error",
            "reason": "verification pipeline failure"
        }


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