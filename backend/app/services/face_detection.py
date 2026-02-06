from app.services.face_model import face_app

def detect_face(frame):
    faces = face_app.get(frame)
    return len(faces) == 1

