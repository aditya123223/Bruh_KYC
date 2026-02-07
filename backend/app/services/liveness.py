import numpy as np
from app.services.embedding import get_embedding


def simple_liveness_check(frames):
    """
    Demo-safe liveness check using:
    - face presence ratio
    - motion energy
    """

    face_count = 0
    motion_total = 0

    valid_pairs = 0

    # -----------------------
    # face presence check
    # -----------------------

    for frame in frames:

        emb = get_embedding(frame)

        if emb is not None:
            face_count += 1

    face_ratio = face_count / max(1, len(frames))

    # -----------------------
    # motion check
    # -----------------------

    for i in range(len(frames) - 1):

        f1 = frames[i].astype(float)
        f2 = frames[i + 1].astype(float)

        diff = np.mean(np.abs(f1 - f2))

        motion_total += diff
        valid_pairs += 1

    motion_score = motion_total / max(1, valid_pairs)

    print("Liveness Debug → face_ratio:", face_ratio)
    print("Liveness Debug → motion_score:", motion_score)

    # -----------------------
    # thresholds (demo tuned)
    # -----------------------

    FACE_THRESHOLD = 0.6
    MOTION_THRESHOLD = 4.0

    live = (
        face_ratio >= FACE_THRESHOLD
        and motion_score >= MOTION_THRESHOLD
    )

    return {
        "is_live": live,
        "face_ratio": face_ratio,
        "motion_score": motion_score
    }




