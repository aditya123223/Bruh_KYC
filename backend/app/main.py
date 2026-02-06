from fastapi import FastAPI
from app.api.kyc import router

app = FastAPI(title="KYC Verification Backend")

app.include_router(router)

@app.get("/")
def root():
    return {"status": "KYC backend running"}
