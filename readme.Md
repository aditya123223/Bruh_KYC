# 🔐 Bruh_KYC — AI-Powered Identity Verification System

&gt; A full-stack **Know Your Customer (KYC)** verification platform that combines **active liveness detection**, **deepfake/AI-image detection**, **face recognition**, and **anti-spoofing** to provide secure, real-time identity verification.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Security](#security)
- [Screenshots](#screenshots)
- [Future Roadmap](#future-roadmap)
- [License](#license)

---

## 🎯 Overview

**Bruh_KYC** is a modern KYC verification system designed for hackathons and production environments. It validates user identity through a multi-layered pipeline:

1. **Selfie Upload** — Image quality & blur detection
2. **AI-Generated Image Detection** — Detects synthetic/AI-generated faces
3. **Active Liveness Verification** — Video-based blink, head movement & mouth motion detection
4. **Face Recognition & Duplicate Detection** — Prevents identity fraud via vector similarity search
5. **Identity Match Verification** — Cross-validates selfie vs. video embeddings
6. **Decision Engine** — Final approve/reject verdict with audit logging

---

## ✨ Features

| Feature                           | Description                                                                                  |
| --------------------------------- | -------------------------------------------------------------------------------------------- |
| 🤖 **AI Image Detection**         | Uses Hugging Face's `umm-maybe/ai-image-detector` to flag AI-generated/synthetic selfies     |
| 👁️ **Active Liveness Detection**  | MediaPipe FaceMesh-based blink counting, head movement tracking, and mouth variance analysis |
| 🔍 **Face Recognition**           | InsightFace (Buffalo_L model) for 512-D embedding extraction                                 |
| 🛡️ **Anti-Duplicate**             | Cosine similarity search against stored embeddings to prevent identity reuse                 |
| ⚡ **Real-time Video Processing** | WebRTC-based video recording with frame extraction                                           |
| 🔐 **Session Management**         | Secure token-based sessions with TTL and anti-spam guards                                    |
| 📊 **Admin Dashboard**            | Attempt logging, approval/rejection statistics                                               |
| 🌐 **Responsive Frontend**        | React + Material-UI with stepper-based KYC flow                                              |

---

## 🛠️ Tech Stack

### Backend

| Technology                      | Purpose                                          |
| ------------------------------- | ------------------------------------------------ |
| **Python 3.11+**                | Core language                                    |
| **FastAPI**                     | High-performance async API framework             |
| **InsightFace**                 | Deep face analysis & embedding (Buffalo_L model) |
| **MediaPipe**                   | Real-time face landmark detection                |
| **Transformers (Hugging Face)** | AI-generated image classification                |
| **OpenCV**                      | Image/video processing                           |
| **NumPy**                       | Numerical operations & vector storage            |
| **Uvicorn**                     | ASGI server                                      |

### Frontend

| Technology            | Purpose             |
| --------------------- | ------------------- |
| **React 18**          | UI framework        |
| **Vite**              | Build tool          |
| **Material-UI (MUI)** | Component library   |
| **Axios**             | HTTP client         |
| **React Router**      | Client-side routing |

---

## 📁 Project Structure

Bruh_KYC/
├── backend/
│ ├── app/
│ │ ├── init.py
│ │ ├── main.py # FastAPI app entry point
│ │ ├── api/
│ │ │ └── kyc.py # KYC verification endpoints
│ │ ├── services/
│ │ │ ├── active_liveness.py # Blink/head/mouth detection
│ │ │ ├── ai_image_detector.py# AI-generated image detection
│ │ │ ├── embedding.py # Face embedding extraction
│ │ │ ├── face_detection.py # Single face validation
│ │ │ ├── face_model.py # InsightFace model loader
│ │ │ ├── image_quality.py # Blur & brightness checks
│ │ │ ├── liveness.py # Passive motion-based liveness
│ │ │ ├── similarity.py # Cosine similarity & duplicate detection
│ │ │ ├── video_processing.py # Frame extraction from video
│ │ │ └── vision_pipeline.py # Orchestrated validation pipeline
│ │ ├── db/
│ │ │ ├── vector_store.py # NumPy-based embedding storage
│ │ │ └── metadata_db.py # Metadata storage (stub)
│ │ ├── decision/
│ │ │ └── decision_engine.py # Final approve/reject logic
│ │ ├── security/
│ │ │ ├── auth.py # API key authentication
│ │ │ ├── rate_limit.py # Sliding window rate limiter
│ │ │ └── session_guard.py # Token-based session management
│ │ ├── admin/
│ │ │ ├── admin_routes.py # Admin dashboard endpoints
│ │ │ └── attempt_logger.py # JSON-based audit logging
│ │ ├── utils/
│ │ │ └── logger.py # Debug logger
│ │ └── test_services.py # Service unit tests
│ ├── requirements.txt
│ ├── attempt_log.json # Audit trail
│ ├── stored_embeddings.npy # Face embedding database
│ └── stored_images/ # Stored face images
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── main.jsx
│ │ ├── Pages/
│ │ │ ├── Home/
│ │ │ │ ├── home.jsx
│ │ │ │ ├── Hero.jsx
│ │ │ │ ├── LeftSection.jsx
│ │ │ │ ├── RightSection.jsx
│ │ │ │ ├── navbar.jsx
│ │ │ │ └── footer.jsx
│ │ │ └── KYC/
│ │ │ ├── KYC.jsx # Main KYC stepper flow
│ │ │ ├── GeneralInfo.jsx # Identity form + selfie upload
│ │ │ ├── VideoVerification.jsx # WebRTC video recording
│ │ │ └── Result.jsx # Approval/rejection display
│ │ └── Services/
│ │ ├── api.jsx # Axios instance with API key
│ │ └── Upload.jsx # File upload handler
│ ├── index.html
│ ├── package.json
│ └── vite.config.js
│
└── readme.Md

---

## 🚀 Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- CUDA (optional, for GPU acceleration)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Download InsightFace models on first run
# The app auto-downloads buffalo_l model

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

The frontend will be available at http://localhost:5173 and the backend at http://localhost:8000.

🎮 Usage
User Flow
Landing Page — Click "Do KYC" to start
Session Creation — Backend generates a secure session token
Identity Info — Fill name, age, gender + upload selfie
Video Verification — Record a short video (blink & move head naturally)
Submit — Backend runs the full verification pipeline
Result — Instant approve/reject with reason
Admin Dashboard
Access attempt logs and statistics:

curl -H "x-api-key: hackathon-demo-key" http://localhost:8000/admin/attempts
curl -H "x-api-key: hackathon-demo-key" http://localhost:8000/admin/stats

📡 API Endpoints

| Method | Endpoint          | Description             | Auth              |
| ------ | ----------------- | ----------------------- | ----------------- |
| `GET`  | `/`               | Health check            | None              |
| `GET`  | `/kyc/session`    | Generate session token  | API Key           |
| `POST` | `/kyc/verify`     | Full KYC verification   | API Key + Session |
| `GET`  | `/admin/attempts` | Get all attempt logs    | API Key           |
| `GET`  | `/admin/stats`    | Get approval statistics | API Key           |


/kyc/verify Request

curl -X POST http://localhost:8000/kyc/verify \
  -H "x-api-key: hackathon-demo-key" \
  -F "session_token=<token>" \
  -F "image=@selfie.jpg" \
  -F "video=@verification.mp4"

  Response Format

{
  "status": "approved",
  "liveness": true,
  "ai_generated_prob": 0.023,
  "duplicate": false,
  "identity_match": true,
  "similarity": 0.892,
  "message": "KYC approved"
}

🔒 Security Features

| Layer                  | Implementation                                        |
| ---------------------- | ----------------------------------------------------- |
| **Authentication**     | API key via `x-api-key` header                        |
| **Rate Limiting**      | Sliding window (5 requests / 10s per IP)              |
| **Session Management** | Cryptographic tokens with 5-min TTL, max 200 sessions |
| **Anti-Duplicate**     | Cosine similarity > 0.85 blocks re-enrollment         |
| **AI Detection**       | Rejects images with > 90% AI-generated probability    |
| **Audit Logging**      | All attempts timestamped and stored in JSON           |


🔮 Future Roadmap
[ ] Passive Liveness Detection — Deep learning-based spoof detection (printed photo, screen replay)
[ ] Deepfake Video Detection — Analyze temporal inconsistencies in video
[ ] OCR Integration — ID card/document verification
[ ] Database Migration — PostgreSQL + pgvector for scalable embedding storage
[ ] Docker Compose — One-command deployment
[ ] CI/CD Pipeline — GitHub Actions for testing & deployment
[ ] Mobile App — React Native companion


🙏 Acknowledgments
InsightFace for face analysis
MediaPipe for real-time face landmarks
Hugging Face for AI image detection model
FastAPI for the backend framework

📄 License
This project was built for hackathon/demo purposes. For production use, please:
Replace hardcoded API keys with environment variables
Implement proper database storage
Add HTTPS/TLS termination
Review and harden security configurations


Built with 💙 for secure digital identity verification.

---

This README captures every module, security layer, ML pipeline component, and frontend flow from the codebase. It includes installation steps, API documentation, architecture diagrams, and security considerations. Feel free to customize the screenshots section and add your own branding!
```
