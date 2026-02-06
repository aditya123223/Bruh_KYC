<<<<<<< HEAD
# backend/app/api/kyc.py

from app.services.active_liveness import active_liveness_from_video
import tempfile
import os

=======
>>>>>>> c337a317439d7951be677d83e479b573b83fbe00
from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2
import asyncio

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


# =============================
# async image reader (SAFE)
# =============================

async def read_image(upload: UploadFile):
    contents = await upload.read()
    arr = np.frombuffer(contents, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


# =============================
# IMAGE VERIFY
# =============================

@router.post("/verify")
async def verify(image1: UploadFile = File(...),
                 image2: UploadFile = File(...)):

    try:
        log("Image verification started")

        frame1 = await read_image(image1)
        frame2 = await read_image(image2)

        if frame1 is None or frame2 is None:
            return {"status": "rejected", "reason": "invalid image"}

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

        duplicate = await asyncio.to_thread(check_duplicate, embedding)

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


# =============================
# SEARCH
# =============================

@router.post("/search")
async def search(image: UploadFile = File(...)):

    try:
        log("Identity search started")

        frame = await read_image(image)

        if frame is None:
            return {"status": "error", "reason": "invalid image"}

        embedding = await asyncio.to_thread(get_embedding, frame)

        if embedding is None:
            return {"status": "rejected", "reason": "encoding failed"}

        match, score = await asyncio.to_thread(search_face, embedding)

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


# =============================
# VIDEO VERIFY
# =============================

@router.post("/verify-video")
async def verify_video(video: UploadFile = File(...)):

    try:
        log("Layered video verification started")

<<<<<<< HEAD
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
=======
        frames = await asyncio.to_thread(extract_frames, video)

        if not frames or len(frames) < 2:
            return {"status": "rejected", "reason": "not enough frames"}

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
>>>>>>> c337a317439d7951be677d83e479b573b83fbe00

        if embedding is None:
            return {"status": "error", "reason": "embedding failure"}

        duplicate = await asyncio.to_thread(check_duplicate, embedding)

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


# =============================
# REGISTRY
# =============================

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
