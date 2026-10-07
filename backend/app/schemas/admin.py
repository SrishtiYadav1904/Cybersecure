from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import datetime

class CategoryStat(BaseModel):
    category: str
    count: int
    percentage: float

class LanguageStat(BaseModel):
    language: str
    count: int
    percentage: float

class PlatformStat(BaseModel):
    platform: str
    count: int

class AdminDashboardStats(BaseModel):
    total_users: int
    total_incidents: int
    bullying_detections: int
    non_bullying_detections: int
    help_requests: int
    active_support_sessions: int
    class_distribution: List[CategoryStat]
    language_distribution: List[LanguageStat]
    platform_distribution: List[PlatformStat]
    average_confidence: float
    current_model_version: str
    drift_status: str

class ModelVersionResponse(BaseModel):
    id: int
    version_tag: str
    model_name: str
    training_date: datetime.datetime
    dataset_version: str
    features_description: str
    macro_f1: float
    pr_auc: float
    accuracy: float
    is_active: bool

    model_config = {"protected_namespaces": (), "from_attributes": True}

class SlangTermResponse(BaseModel):
    id: int
    term: str
    language: str
    candidate_meaning: Optional[str] = None
    frequency: int
    status: str
    sample_context: Optional[str] = None
    first_seen: datetime.datetime
    approved_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class DriftEventResponse(BaseModel):
    id: int
    metric_name: str
    metric_value: float
    drift_status: str
    affected_classes_json: Optional[Any] = None
    sample_size: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True
