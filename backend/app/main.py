import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.database.session import engine, Base, SessionLocal
from backend.app.database.models import User, Resource, ModelVersion
from backend.app.auth.security import get_password_hash

# Routers
from backend.app.api.auth import router as auth_router
from backend.app.api.analyze import router as analyze_router
from backend.app.api.incidents import router as incidents_router
from backend.app.api.reports import router as reports_router
from backend.app.api.support import router as support_router
from backend.app.api.help_requests import router as help_router
from backend.app.api.admin import router as admin_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Multilingual Explainable Cyberbullying Detection, Incident Management & Support System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow development frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(incidents_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(support_router, prefix="/api")
app.include_router(help_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

# Static uploads directory mount
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.on_event("startup")
def on_startup():
    # 1. Initialize database tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 2. Seed Default Administrator if not present
        admin_user = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin_user:
            admin_user = User(
                email=settings.ADMIN_EMAIL,
                username="admin",
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                full_name=settings.ADMIN_NAME,
                role="ADMIN",
                is_active=True
            )
            db.add(admin_user)
            db.commit()

        # 3. Seed Production and Baseline Model Versions
        models_to_seed = [
            {
                "version_tag": "CB-EXP-002",
                "model_name": "CyberGuard Production Expanded Stacking Ensemble",
                "dataset_version": "CB-DATA-002",
                "features_description": "PCA(GloVe 100d->30d) + Contextual(384d) -> Fusion(414d) -> Stacking (SVM, XGBoost, LightGBM, CatBoost)",
                "macro_f1": 0.7081,
                "pr_auc": 0.7718,
                "accuracy": 0.7553,
                "is_active": True
            },
            {
                "version_tag": "CB-BASE-001",
                "model_name": "CyberGuard Baseline Stacking Ensemble",
                "dataset_version": "CB-DATA-001",
                "features_description": "PCA(GloVe 100d->30d) + Contextual(384d) -> Fusion(414d) -> Stacking AML",
                "macro_f1": 0.9711,
                "pr_auc": 0.9968,
                "accuracy": 0.9706,
                "is_active": False
            },
            {
                "version_tag": "SUP-001",
                "model_name": "CyberGuard Wellbeing Support Intelligence Family",
                "dataset_version": "WB-DATA-001",
                "features_description": "Contextual Semantic Encoder(384d) -> Crisis Triage + LoST Distress + Stress Calibrator",
                "macro_f1": 0.6936,
                "pr_auc": 0.7500,
                "accuracy": 0.7803,
                "is_active": True
            }
        ]

        for m_dict in models_to_seed:
            existing = db.query(ModelVersion).filter(ModelVersion.version_tag == m_dict["version_tag"]).first()
            if not existing:
                mv = ModelVersion(
                    version_tag=m_dict["version_tag"],
                    model_name=m_dict["model_name"],
                    dataset_version=m_dict["dataset_version"],
                    features_description=m_dict["features_description"],
                    macro_f1=m_dict["macro_f1"],
                    pr_auc=m_dict["pr_auc"],
                    accuracy=m_dict["accuracy"],
                    is_active=m_dict["is_active"]
                )
                db.add(mv)
        db.commit()

        # 4. Seed Official Resources from resources.json
        res_count = db.query(Resource).count()
        if res_count == 0:
            res_json_path = os.path.join(settings.KNOWLEDGE_BASE_DIR, "resources", "resources.json")
            helplines_file = os.path.join(settings.KNOWLEDGE_BASE_DIR, "emergency_resources", "helplines.json")
            target_file = res_json_path if os.path.exists(res_json_path) else helplines_file
            if os.path.exists(target_file):
                with open(target_file, "r", encoding="utf-8") as f:
                    res_data = json.load(f)
                    for item in res_data:
                        r = Resource(
                            category=item.get("category", "CRISIS_COUNSELING"),
                            name=item.get("resource_name") or item.get("name", "Helpline"),
                            contact_number=item.get("phone") or item.get("contact_number"),
                            website=item.get("url") or item.get("website"),
                            description=item.get("description"),
                            is_emergency=("14416" in str(item.get("phone", "")) or "1930" in str(item.get("phone", ""))),
                            is_active=item.get("active_status", True)
                        )
                        db.add(r)
                    db.commit()
    finally:
        db.close()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "active_model_version": settings.ACTIVE_MODEL_VERSION
    }
