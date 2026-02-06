import cv2
import numpy as np

# tune based on environment
BLUR_THRESHOLD = 80
BRIGHT_MIN = 70
BRIGHT_MAX = 180


def check_image_quality(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # --- blur detection ---
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # --- brightness detection ---
    brightness = np.mean(gray)

    print("Blur score:", blur_score)
    print("Brightness:", brightness)

    # blur rejection
    if blur_score < BLUR_THRESHOLD:
        return False

    # brightness rejection
    if brightness < BRIGHT_MIN or brightness > BRIGHT_MAX:
        return False

    return True


