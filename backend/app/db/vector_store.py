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
    if os.path.exists(DB_PATH):
        return list(np.load(DB_PATH, allow_pickle=True))
    return []


def save_db(db):
    np.save(DB_PATH, db)


def store_face(frame, embedding):
    os.makedirs(IMAGE_DIR, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(IMAGE_DIR, filename)

    cv2.imwrite(path, frame)

    db = load_db()
    db.append(embedding)
    save_db(db)

    return filename


# -------------------------
# Registry helpers
# -------------------------

def get_identity_count():
    return len(load_db())


def list_identities():
    if not os.path.exists(IMAGE_DIR):
        return []

    return [os.path.basename(f) for f in glob.glob(f"{IMAGE_DIR}/*.jpg")]


def reset_registry():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    if os.path.exists(IMAGE_DIR):
        for f in os.listdir(IMAGE_DIR):
            os.remove(os.path.join(IMAGE_DIR, f))