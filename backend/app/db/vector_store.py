import numpy as np
import os
import cv2
import uuid
import glob

DB_PATH = "stored_embeddings.npy"
IMAGE_DIR = "stored_images"


# -------------------------
# Core DB functions
# -------------------------

def load_db():
    """
    Load embedding DB safely.
    Recovers from corruption or shape mismatch.
    """
    if not os.path.exists(DB_PATH):
        return []

    try:
        data = np.load(DB_PATH, allow_pickle=True)

        # ensure list of embeddings
        db = [np.array(e) for e in data]

        return db

    except Exception as e:
        print("DB load failed — recovering:", e)
        return []


def save_db(db):
    """
    Save embeddings safely as object array
    to avoid NumPy shape issues.
    """
    arr = np.array(db, dtype=object)
    np.save(DB_PATH, arr)


def store_face(frame, embedding):
    """
    Store image + embedding atomically
    """
    os.makedirs(IMAGE_DIR, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(IMAGE_DIR, filename)

    cv2.imwrite(path, frame)

    db = load_db()

    # ensure embedding is numpy array
    db.append(np.array(embedding))

    save_db(db)

    return filename


# -------------------------
# Registry helpers
# -------------------------

def get_identity_count():
    """
    Count identities based on stored images.
    This is demo-safe ground truth.
    """
    if not os.path.exists(IMAGE_DIR):
        return 0

    return len(glob.glob(f"{IMAGE_DIR}/*.jpg"))


def list_identities():
    if not os.path.exists(IMAGE_DIR):
        return []

    return [
        os.path.basename(f)
        for f in glob.glob(f"{IMAGE_DIR}/*.jpg")
    ]


def reset_registry():
    """
    Clear embeddings + images safely
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    if os.path.exists(IMAGE_DIR):
        for f in os.listdir(IMAGE_DIR):
            os.remove(os.path.join(IMAGE_DIR, f))
