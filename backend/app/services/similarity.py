import numpy as np
from app.db.vector_store import load_db

SIM_THRESHOLD = 0.6


def cosine_similarity(a, b):

    den = np.linalg.norm(a) * np.linalg.norm(b)

    if den == 0:
        return 0.0

    return np.dot(a, b) / den


def check_duplicate(new_emb):

    db = load_db()

    for emb in db:
        score = cosine_similarity(new_emb, emb)

        if score > SIM_THRESHOLD:
            return True

    return False


def search_face(new_emb):

    db = load_db()

    if not db:
        return False, 0.0

    best_score = -1

    for emb in db:
        score = cosine_similarity(new_emb, emb)
        best_score = max(best_score, score)

    if best_score > SIM_THRESHOLD:
        return True, best_score

    return False, best_score



