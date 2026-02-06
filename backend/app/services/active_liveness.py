import cv2
import numpy as np
import os
from collections import deque
from mediapipe.python.solutions import face_mesh

# ------------------ MediaPipe Setup ------------------
face_mesh_model = face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

# ------------------ Parameters ------------------
EAR_THRESHOLD = 0.20
BLINK_MIN_FRAMES = 2
MIN_CONFIDENCE_SCORE = 0.4
MAX_FRAMES = 180

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]
NOSE_IDX = 1
MOUTH_TOP = 13
MOUTH_BOTTOM = 14

# ------------------ Utility Functions ------------------
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def compute_head_movement(points):
    if len(points) < 2:
        return 0.0
    diffs = [
        np.linalg.norm(points[i] - points[i - 1])
        for i in range(1, len(points))
    ]
    return float(np.mean(diffs))

# ------------------ Main Liveness Function ------------------
def active_liveness_from_video(video_path):
    if not os.path.exists(video_path):
        return {"error": "video_not_found"}

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "cannot_open_video"}

    blink_counter = 0
    total_blinks = 0

    nose_positions = deque(maxlen=20)
    mouth_movements = []

    frames = 0

    while cap.isOpened() and frames < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret:
            break

        frames += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh_model.process(rgb)

        if not result.multi_face_landmarks:
            continue

        lm = result.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        def pt(i):
            return np.array([lm[i].x * w, lm[i].y * h])

        # ------------------ Blink Detection ------------------
        left_eye = np.array([pt(i) for i in LEFT_EYE])
        right_eye = np.array([pt(i) for i in RIGHT_EYE])

        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2

        if ear < EAR_THRESHOLD:
            blink_counter += 1
        else:
            if blink_counter >= BLINK_MIN_FRAMES:
                total_blinks += 1
            blink_counter = 0

        # ------------------ Head Movement ------------------
        nose_positions.append(pt(NOSE_IDX))

        # ------------------ Mouth Movement ------------------
        mouth_open = np.linalg.norm(pt(MOUTH_TOP) - pt(MOUTH_BOTTOM))
        mouth_movements.append(mouth_open)

    cap.release()

    # ------------------ Motion Metrics ------------------
    head_movement = compute_head_movement(list(nose_positions))

    jitter = np.std([
        np.linalg.norm(nose_positions[i] - nose_positions[i - 1])
        for i in range(1, len(nose_positions))
    ]) if len(nose_positions) > 5 else 0.0

    mouth_variance = np.std(mouth_movements) if len(mouth_movements) > 5 else 0.0

    # ------------------ Confidence Scoring ------------------
    score = 0.0
    score += min(1.0, total_blinks / 2) * 0.30
    score += min(1.0, head_movement / 3) * 0.30
    score += min(1.0, jitter / 1.0) * 0.20
    score += min(1.0, mouth_variance / 3.0) * 0.10

    is_live = score >= MIN_CONFIDENCE_SCORE

    return {
        "is_live": bool(is_live),
        "confidence": round(score, 2),
        "blink_count": total_blinks,
        "head_movement": round(head_movement, 2),
        "motion_jitter": round(float(jitter), 3),
        "mouth_variance": round(float(mouth_variance), 2),
        "frames_processed": frames,
    }

# ------------------ TEST ------------------
if __name__ == "__main__":
    result = active_liveness_from_video("C:/Users/vikram/OneDrive/Desktop/test/sample4.mp4")
    print(result)