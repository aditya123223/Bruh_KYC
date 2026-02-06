import cv2
import numpy as np

# Demo-friendly thresholds
BLUR_THRESHOLD = 20     # lowered for webcams
BRIGHT_MIN = 40
BRIGHT_MAX = 220


def check_image_quality(frame):
    """
    Returns:
        (is_valid, reason)
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -----------------
    # Blur detection
    # -----------------
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # -----------------
    # Brightness detection
    # -----------------
    brightness = np.mean(gray)

    print("Quality Debug → blur:", blur_score, "brightness:", brightness)

    # blur rejection
    if blur_score < BLUR_THRESHOLD:
        return False, "image blurry"

    # brightness rejection
    if brightness < BRIGHT_MIN:
        return False, "too dark"

    if brightness > BRIGHT_MAX:
        return False, "too bright"

    return True, None



