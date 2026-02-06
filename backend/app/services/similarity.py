import numpy as np
from app.db.vector_store import load_db

# cosine similarity threshold
SIM_THRESHOLD = 0.6


def cosine_similarity(a, b):
    """
    Compute cosine similarity between two embeddings
    """
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def check_duplicate(new_emb):
    """
    Returns True if duplicate identity detected
    """
    db = load_db()

    for emb in db:
        score = cosine_similarity(new_emb, emb)

        if score > SIM_THRESHOLD:
            return True

    return False


def search_face(new_emb):
    """
    Search best match in database

    Returns:
        (match_found, similarity_score)
    """
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


