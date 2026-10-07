# CyberGuard — Universal Setup & Project Transfer Guide

> **This document is designed for anyone opening, running, or developing CyberGuard on a new or different computer (Windows, macOS, or Linux) with ZERO file path errors.**

---

## 📑 Table of Contents
1. [Project Overview & Architecture](#1-project-overview--architecture)
2. [How Path Independence Works (Why There Are No Path Errors)](#2-how-path-independence-works)
3. [Packaging & Sharing the Project](#3-packaging--sharing-the-project)
4. [Prerequisites on the New Device](#4-prerequisites-on-the-new-device)
5. [Universal 1-Step Quickstart (Recommended)](#5-universal-1-step-quickstart-recommended)
6. [Alternative Ways to Run](#6-alternative-ways-to-run)
   - [Option A: Windows Batch Launcher (`.bat`)](#option-a-windows-batch-launcher)
   - [Option B: macOS / Linux Shell Launcher (`.sh`)](#option-b-macos--linux-shell-launcher)
   - [Option C: VS Code Direct Run (Tasks / Launch)](#option-c-vs-code-direct-run)
   - [Option D: Manual Terminal Execution (2 Terminals)](#option-d-manual-terminal-execution)
7. [Default Logins & Access Credentials](#7-default-logins--access-credentials)
8. [Project Directory & File Structure](#8-project-directory--file-structure)
9. [Configuration & Environment Variables (`.env`)](#9-configuration--environment-variables)
10. [Troubleshooting & FAQ](#10-troubleshooting--faq)

---

## 1. Project Overview & Architecture

**CyberGuard** is an enterprise-grade AI cybersecurity and victim support platform engineered for:
- **Multilingual Cyberbullying Detection**: Detects cyberbullying across English, Hindi (Devanagari), and Hinglish (code-mixed Romanized Hindi).
- **10 Fine-Grained Toxicity Classes**: Age, Gender, Religion, Ethnicity, Appearance, Mockery/Defamation, Abusive/Insult, Threat/Intimidation, Personal Harassment, and Non-Bullying.
- **Multimodal Screenshot Analysis**: Upload screenshots from WhatsApp, Instagram, Twitter/X, or Discord. Deep-learning OCR (RapidOCR / EasyOCR / PyTesseract) extracts text and runs classification.
- **Explainable AI (XAI)**: Highlights offensive tokens, provides saliency scores, confidence meters, and confidence gauge arcs.
- **Group Chat / Thread Triage**: Analyzes multi-message conversation transcripts to highlight high-risk participants.
- **Incident Preservation & Forensic PDF Export**: Creates tamper-evident, SHA-256 verified PDF evidence reports compliant with legal reporting standards.
- **Dual Wellbeing Support Intelligence**: Grounded crisis response engine, helpline dialers (Tele-MANAS `14416`, Cybercrime `1930`), and triage counselor chat.
- **Admin Operations Hub**: Drift monitoring, model registry inspection, slang submission approvals, and security audit logs.

### Technical Stack
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, SQLite, Pydantic v2, Uvicorn, ReportLab.
- **Machine Learning**: Scikit-Learn, LightGBM, XGBoost, CatBoost, GloVe + Contextual embeddings, PCA dimensionality reduction.
- **Frontend**: React 18, Vite 5, Tailwind CSS, Lucide React icons.

---

## 2. How Path Independence Works

In many projects, moving files to another user's machine causes path errors (e.g. `C:\Users\username\... not found`). 
**In CyberGuard, this has been engineered away completely:**

1. **Dynamic Project Root Resolution**: `backend/app/config.py` computes `BASE_DIR = Path(__file__).resolve().parent.parent.parent` dynamically. All directories (`uploads/`, `artifacts/`, `trained_models/`, `cyberguard.db`) resolve relative to the installation directory on whatever machine it is running on.
2. **Relative SQLite Binding**: The SQLite database string `sqlite:///./cyberguard.db` is automatically resolved to an absolute URI at runtime, preventing duplicate empty databases when running from subdirectories.
3. **Frontend Vite Reverse Proxy**: Frontend network calls use relative paths (`/api/...`). The Vite development server automatically proxies these requests to `http://127.0.0.1:8000`, completely avoiding CORS errors and hardcoded URLs.
4. **Universal Runner (`run.py`)**: A portable launcher detects the host operating system, resolves paths, checks dependencies, and launches both services together.

---

## 3. Packaging & Sharing the Project

When sending this project folder to your friend (via Google Drive, ZIP, USB, or Git), **save bandwidth and prevent system conflicts by excluding heavy generated folders**:

### ✅ DO Include:
- `backend/` (FastAPI source code)
- `frontend/` (React source code, `package.json`, `index.html`, `vite.config.js`)
- `ml/` (Feature engineering, models, pipeline)
- `trained_models/` (Pre-trained AML model weights and encoders)
- `cyberguard.db` (Database with pre-seeded users and demo data)
- `requirements.txt`
- `.env` and `.env.example`
- `run.py`, `start_windows.bat`, `start_unix.sh`
- `.vscode/` (VS Code task and launch settings)

### ❌ DO NOT Include (Delete or Exclude before zipping):
- `frontend/node_modules/` (Very large! Your friend will re-install in 30 seconds via `npm install`)
- `.venv/` or `venv/` (Python virtual environments cannot be copied across machines or different user accounts)
- `__pycache__/` (Compiled Python bytecode)
- `.pytest_cache/`

> **Note**: Even if `cyberguard.db` is missing, CyberGuard will automatically create a brand new SQLite database and seed the default Administrator account on startup.

---

## 4. Prerequisites on the New Device

Before starting, the target device needs:

1. **Python 3.10 or higher**:
   - Download: [python.org](https://www.python.org/downloads/)
   - *Windows note*: Check the box **"Add python.exe to PATH"** during installation.
2. **Node.js 18 or higher** (includes `npm`):
   - Download: [nodejs.org](https://nodejs.org/) (LTS recommended)
3. *(Optional)* **Tesseract OCR** (Only if you do not want to use the built-in RapidOCR / EasyOCR engines).

---

## 5. Universal 1-Step Quickstart (Recommended)

This is the easiest, zero-error method. It works on **Windows, macOS, and Linux**.

### Step 1: Open Terminal in the Project Folder
Open your terminal (PowerShell, Command Prompt, or Terminal) in the extracted `cyberguard` directory.

### Step 2: Set up Python Virtual Environment (One-time)
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Backend Requirements (One-time)
```bash
pip install -r requirements.txt
```

### Step 4: Run the Universal Launcher
```bash
python run.py
```
*(On macOS/Linux, you can also run `python3 run.py`)*

**What `run.py` does automatically:**
- Verifies Python and Node.js versions.
- Automatically runs `npm install` inside `frontend/` if `node_modules` is not yet installed.
- Starts the FastAPI Backend at `http://127.0.0.1:8000`.
- Starts the Vite Frontend at `http://127.0.0.1:5173`.
- Prints portal credentials and links to the console.
- Gracefully terminates both servers when you press `Ctrl+C`.

---

## 6. Alternative Ways to Run

### Option A: Windows Batch Launcher
If you are on Windows, simply double-click:
```
start_windows.bat
```
*(Or execute `.\start_windows.bat` in Command Prompt / PowerShell).*

---

### Option B: macOS / Linux Shell Launcher
On macOS or Linux:
```bash
chmod +x start_unix.sh
./start_unix.sh
```

---

### Option C: VS Code Direct Run
1. Open VS Code.
2. Select **File → Open Folder...** and pick the `cyberguard` root directory.
3. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
4. Type **Tasks: Run Task** and choose:
   - **`Run CyberGuard (Universal)`** — Runs both backend and frontend together!
5. Or to debug the backend, press **F5** (uses `.vscode/launch.json`).

---

### Option D: Manual Terminal Execution (2 Terminals)

If you prefer full control in separate terminal tabs:

#### Terminal 1 — Backend (FastAPI)
```bash
# 1. Navigate to project root
cd /path/to/cyberguard

# 2. Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Launch FastAPI backend
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend is live at:* `http://127.0.0.1:8000`  
*Interactive Swagger docs:* `http://127.0.0.1:8000/docs`

#### Terminal 2 — Frontend (Vite + React)
```bash
# 1. Navigate to frontend directory
cd /path/to/cyberguard/frontend

# 2. Install dependencies (first time only)
npm install

# 3. Launch dev server
npm run dev
```
*Frontend is live at:* `http://127.0.0.1:5173`

---

## 7. Default Logins & Access Credentials

The application includes pre-configured role accounts:

| Portal / Role | Email / Username | Password | Features Accessible |
|---|---|---|---|
| **System Administrator** | `admin@cyberguard.ai` | `AdminSecure2026!` | Admin Analytics, Model Registry, Drift Diagnostics, Slang Approvals, User Audit Logs, Full System Overview |
| **Analyst / Demo User** | `analyst@cyberguard.ai` | Click **"Analyst Demo"** on login | Text Detection, Screenshot OCR, Group Chat Analysis, Incident Timeline, PDF Generation, Wellbeing Counselor |
| **Standard User** | Register any new email | Any chosen password | Personal Safety Portal, Report Generation, Anonymous Support Sessions |
| **Consultant** | `consultant@cyberguard.ai` | `Consultant2026!` | Escalated Crisis Cases, High-Risk Victim Triage |

> 💡 **Quick Login Tip**: On the login screen (`http://127.0.0.1:5173`), you can click the **"Admin Demo"** or **"Analyst Demo"** buttons to auto-populate credentials and log in instantly with one click.

---

## 8. Project Directory & File Structure

```text
cyberguard/
│
├── backend/                  # FastAPI Application
│   └── app/
│       ├── api/              # Endpoints: auth, analyze, incidents, reports, support, admin
│       ├── auth/             # JWT security, password hashing, RBAC permissions
│       ├── database/         # SQLAlchemy models, SQLite session management
│       ├── ocr/              # Multi-tier OCR engine (RapidOCR, EasyOCR, Tesseract)
│       ├── reports/          # Forensic PDF report generator (ReportLab + SHA-256)
│       ├── support/          # Grounded crisis wellbeing support & hotlines
│       ├── config.py         # Dynamic path normalization (Base directory anchor)
│       └── main.py           # FastAPI application entrypoint & startup seeders
│
├── frontend/                 # React 18 + Vite 5 Frontend Application
│   ├── src/
│   │   ├── components/       # UI components (Dashboard, Analyze, Incidents, Admin, etc.)
│   │   ├── api.js            # API client with token storage and proxy routing
│   │   ├── App.jsx           # Main layout, role views, navigation
│   │   ├── index.css         # Custom animations, glassmorphism, Tailwind directives
│   │   └── main.jsx          # React DOM entry
│   ├── package.json          # Frontend dependencies & scripts
│   ├── tailwind.config.js    # Tailwind CSS design system configuration
│   └── vite.config.js        # Vite config with /api reverse proxy to port 8000
│
├── ml/                       # Machine Learning & AI Pipeline
│   ├── explainability/       # Token saliency attribution & XAI heatmaps
│   ├── feature_engineering/  # GloVe embeddings, PCA (30d), Contextual encoder (384d)
│   ├── inference/            # CyberGuardMLPipeline unified classifier runner
│   ├── models/               # Stacking ensemble (SVM, LightGBM, XGBoost, CatBoost)
│   ├── preprocessing/        # Normalizer, Devanagari cleaner, language detector
│   └── drift/                # Concept-drift and slang tracking
│
├── trained_models/           # Saved pre-trained model weights (.joblib, .json)
├── knowledge_base/           # Support resources, helpline guides, procedural documents
├── artifacts/                # Generated forensic PDF reports & system artifacts
├── uploads/                  # Uploaded evidence screenshots
├── cyberguard.db             # Pre-seeded SQLite database
├── requirements.txt          # Python dependencies
├── run.py                    # Universal cross-platform launcher
├── start_windows.bat         # 1-click launcher for Windows
├── start_unix.sh             # 1-click launcher for macOS / Linux
├── .env                      # Active runtime environment configuration
└── UNIVERSAL_RUN_GUIDE.md    # This guide
```

---

## 9. Configuration & Environment Variables

The application reads from `.env` in the project root. Default values are pre-configured:

```ini
APP_NAME=CyberGuard
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=cyberguard-super-secret-key-change-in-production-2026-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# SQLite path - Automatically resolved by backend/app/config.py
DATABASE_URL=sqlite:///./cyberguard.db

ACTIVE_MODEL_VERSION=CB-EXP-002
ACTIVE_DATASET_VERSION=CB-DATA-002
DEVICE=cpu
EMBEDDING_DIM=100
PCA_COMPONENTS=30

UPLOAD_DIR=./uploads
ARTIFACTS_DIR=./artifacts
REPORTS_DIR=./artifacts/reports

ADMIN_EMAIL=admin@cyberguard.ai
ADMIN_PASSWORD=AdminSecure2026!
ADMIN_NAME=System Administrator
```

---

## 10. Troubleshooting & FAQ

### Q1: PowerShell says "running scripts is disabled on this system"
**Fix**: Open PowerShell as normal user and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then reactivate your virtual environment.

---

### Q2: Port 8000 or 5173 is already in use
**Fix**: Another application or previous run didn't close cleanly.
- **Windows**:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
  Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process -Force
  ```
- **macOS / Linux**:
  ```bash
  lsof -ti :8000 | xargs kill -9
  lsof -ti :5173 | xargs kill -9
  ```

---

### Q3: `pip install -r requirements.txt` fails on compiled packages (LightGBM/XGBoost)
CyberGuard's pipeline is built with **graceful fallbacks**. If C++ build tools are missing on a minimal system, standard scikit-learn classifiers will step in. 
To install standard wheels without building from source:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --only-binary :all:
```

---

### Q4: "TesseractNotFoundError" when uploading screenshot
CyberGuard automatically tries 3 OCR engines in order:
1. `rapidocr_onnxruntime` (Pure Python/ONNX — recommended, no external software needed)
2. `easyocr` (PyTorch)
3. `pytesseract` (System binary)

If your system lacks Tesseract, install `rapidocr-onnxruntime`:
```bash
pip install rapidocr-onnxruntime
```
CyberGuard will immediately switch to it without needing any system binary or PATH edits.

---

### Q5: "File not found" or "Cannot find cyberguard.db"
Make sure you run commands from the **project root directory** (`cyberguard/`), or run using `python run.py`. `backend/app/config.py` anchors all paths to `BASE_DIR`, so running `python run.py` will always find every file reliably.

---

### ✅ Summary Checklist for Your Friend
1. Extract the `cyberguard` folder.
2. Open terminal in `cyberguard/`.
3. Create & activate venv: `python -m venv .venv` then activate.
4. Install requirements: `pip install -r requirements.txt`.
5. Run: `python run.py`.
6. Open browser at: **`http://127.0.0.1:5173`**.
7. Click **"Admin Demo"** or **"Analyst Demo"** and explore!
