from fastapi import FastAPI
from app.api.kyc import router
from app.admin.admin_routes import router as admin_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="KYC Verification Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # hackathon-safe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"status": "KYC backend running"}
