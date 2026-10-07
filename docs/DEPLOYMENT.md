# CyberGuard Deployment Guide

## 1. Local Development Setup

### 1.1 Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- Git

### 1.2 Backend Initialization
```bash
# Navigate to project root
cd cyberguard

# Create and activate virtual environment (optional)
python -m venv venv
# Windows:
venv\Scripts\activate

# Install Python requirements
pip install -r requirements.txt

# Run dataset download & training scripts (or use pre-generated artifacts)
python scripts/download_datasets.py
python scripts/preprocess_all.py
python scripts/train_cyberbullying.py --mode fast

# Start FastAPI server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 1.3 Frontend Initialization
```bash
cd frontend
npm install
npm run dev
```
Open browser at `http://localhost:5173`.

---

## 2. Docker Deployment
```bash
docker-compose up -d --build
```
This boots:
- PostgreSQL on `localhost:5432`
- FastAPI on `localhost:8000`
- Nginx / React frontend on `localhost:5173`
