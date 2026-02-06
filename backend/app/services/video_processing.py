import cv2
import tempfile
import os


def extract_frames(video_file, max_frames=10):
    """
    Extract frames from uploaded video
    """

    # save temp video file
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp.write(video_file.file.read())
    temp.close()

    cap = cv2.VideoCapture(temp.name)

    frames = []
    count = 0

    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()

        if not ret:
            break

        frames.append(frame)
        count += 1

    cap.release()
    os.remove(temp.name)

    return frames
