# backend/app/services/face_model.py

from insightface.app import FaceAnalysis

face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0)  # GPU=0, CPU=-1
