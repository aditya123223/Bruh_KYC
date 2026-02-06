import cv2
import numpy as np

from app.services.image_quality import check_image_quality
from app.services.face_detection import detect_face
from app.services.liveness import liveness_check
from app.services.embedding import get_embedding
from app.services.similarity import check_duplicate


def load_image(path):
    img = cv2.imread(path)
    if img is None:
        print("❌ Could not load image:", path)
    return img


def test_pipeline(img1_path, img2_path):
    print("\n=== SERVICE TEST PIPELINE ===")

    img1 = load_image(img1_path)
    img2 = load_image(img2_path)

    print("\n🧪 Image Quality Check")
    print("Image 1:", check_image_quality(img1))
    print("Image 2:", check_image_quality(img2))

    print("\n🧪 Face Detection")
    print("Image 1:", detect_face(img1))
    print("Image 2:", detect_face(img2))

    print("\n🧪 Liveness Check")
    print("Movement detected:", liveness_check(img1, img2))

    print("\n🧪 Embedding Extraction")
    emb = get_embedding(img2)

    if emb is None:
        print("❌ Embedding failed")
        return

    print("Embedding size:", len(emb))

    print("\n🧪 Duplicate Check")
    duplicate = check_duplicate(emb)
    print("Duplicate:", duplicate)

    print("\n✅ Service test completed")


if __name__ == "__main__":
    # CHANGE THESE PATHS
    test_pipeline("test1.jpeg", "test2.jpeg")
