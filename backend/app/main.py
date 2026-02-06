from fastapi import FastAPI
from app.api.kyc import router
from app.admin.admin_routes import router as admin_router


app = FastAPI(title="KYC Verification Backend")

app.include_router(router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"status": "KYC backend running"}
