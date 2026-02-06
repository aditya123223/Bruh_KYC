import numpy as np
from app.services.face_model import face_app


def deepfake_risk(frames):
    """
    Returns risk score (0 = safe, 1 = suspicious)
    """

    embeddings = []
    landmark_motion = []

    prev_landmarks = None

    for frame in frames:

        faces = face_app.get(frame)

        if not faces:
            continue

        face = faces[0]

        # embedding consistency
        embeddings.append(face.embedding)

        # landmark jitter
        lm = face.kps

        if prev_landmarks is not None:
            motion = np.linalg.norm(lm - prev_landmarks)
            landmark_motion.append(motion)

        prev_landmarks = lm

    if len(embeddings) < 2:
        return 0.5  # unknown → moderate risk

    # embedding drift
    drift = np.mean([
        np.linalg.norm(embeddings[i] - embeddings[i - 1])
        for i in range(1, len(embeddings))
    ])

    # landmark jitter average
    jitter = np.mean(landmark_motion) if landmark_motion else 0

    # normalize heuristic score
    risk = (drift * 0.5) + (jitter * 0.01)

    print("Deepfake drift:", drift)
    print("Landmark jitter:", jitter)
    print("Risk score:", risk)

    return min(risk, 1.0)

