from insightface.app import FaceAnalysis

face_app = FaceAnalysis(name="buffalo_l")

try:
    face_app.prepare(ctx_id=0)  # GPU
    print("InsightFace running on GPU")
except:
    face_app.prepare(ctx_id=-1)  # CPU fallback
    print("InsightFace running on CPU")

