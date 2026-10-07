import os
from pathlib import Path
from pydantic import BaseModel

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def _resolve_relative_path(path_str: str) -> str:
    p = Path(path_str)
    if not p.is_absolute():
        return str((BASE_DIR / p).resolve())
    return str(p.resolve())

def _resolve_db_url(url_str: str) -> str:
    if url_str.startswith("sqlite:///./") or url_str.startswith("sqlite:///.\\"):
        rel = url_str[len("sqlite:///./"):]
        target = (BASE_DIR / rel).resolve()
        return f"sqlite:///{target.as_posix()}"
    return url_str

class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "CyberGuard")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cyberguard-super-secret-key-change-in-production-2026-secure")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    DATABASE_URL: str = _resolve_db_url(os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR.as_posix()}/cyberguard.db"))
    ACTIVE_MODEL_VERSION: str = os.getenv("ACTIVE_MODEL_VERSION", "CB-EXP-002")
    ACTIVE_DATASET_VERSION: str = os.getenv("ACTIVE_DATASET_VERSION", "CB-DATA-002")
    DEVICE: str = os.getenv("DEVICE", "cpu")
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "100"))
    PCA_COMPONENTS: int = int(os.getenv("PCA_COMPONENTS", "30"))

    UPLOAD_DIR: str = _resolve_relative_path(os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads")))
    ARTIFACTS_DIR: str = _resolve_relative_path(os.getenv("ARTIFACTS_DIR", str(BASE_DIR / "artifacts")))
    REPORTS_DIR: str = _resolve_relative_path(os.getenv("REPORTS_DIR", str(BASE_DIR / "artifacts" / "reports")))
    KNOWLEDGE_BASE_DIR: str = _resolve_relative_path(os.getenv("KNOWLEDGE_BASE_DIR", str(BASE_DIR / "knowledge_base")))
    TRAINED_MODELS_DIR: str = _resolve_relative_path(os.getenv("TRAINED_MODELS_DIR", str(BASE_DIR / "trained_models")))

    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@cyberguard.ai")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "AdminSecure2026!")
    ADMIN_NAME: str = os.getenv("ADMIN_NAME", "System Administrator")

settings = Settings()

# Ensure critical directories exist
for path in [
    settings.UPLOAD_DIR,
    settings.ARTIFACTS_DIR,
    settings.REPORTS_DIR,
    settings.KNOWLEDGE_BASE_DIR,
    settings.TRAINED_MODELS_DIR,
]:
    os.makedirs(path, exist_ok=True)

