# backend/app/services/vision_pipeline.py

from app.services.face_detection import detect_face
from app.services.liveness import liveness_check
from app.services.embedding import get_embedding
from app.services.image_quality import check_image_quality


def run_vision_pipeline(frame1, frame2):
    """
    Runs full vision validation pipeline.

    Returns:
    {
        success: bool,
        liveness: bool,
        embedding: vector or None,
        error: str or None
    }
    """

    # --- Image quality check (stub but future-proof)
    if not check_image_quality(frame1) or not check_image_quality(frame2):
        return {
            "success": False,
            "error": "image too blurry",
            "liveness": False,
            "embedding": None
        }

    # --- Face detection
    if not detect_face(frame1):
        return {
            "success": False,
            "error": "no face detected in image 1",
            "liveness": False,
            "embedding": None
        }

    if not detect_face(frame2):
        return {
            "success": False,
            "error": "no face detected in image 2",
            "liveness": False,
            "embedding": None
        }

    # --- Liveness check
    live = liveness_check(frame1, frame2)

    if not live:
        return {
            "success": False,
            "error": "liveness failed",
            "liveness": False,
            "embedding": None
        }

    # --- Embedding extraction
    embedding = get_embedding(frame2)

    if embedding is None:
        return {
            "success": False,
            "error": "embedding failed",
            "liveness": live,
            "embedding": None
        }

    # --- Success
    return {
        "success": True,
        "error": None,
        "liveness": live,
        "embedding": embedding
    }
