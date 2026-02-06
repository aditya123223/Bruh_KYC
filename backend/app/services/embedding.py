from app.services.face_model import face_app

def get_embedding(frame):
    faces = face_app.get(frame)

    if not faces:
        return None

    return faces[0].embedding
