from typing import List, Optional, Any
from pydantic import BaseModel
import datetime

class EvidenceItemResponse(BaseModel):
    id: int
    evidence_type: str
    file_path: Optional[str] = None
    ocr_raw_text: Optional[str] = None
    edited_text: str
    detected_language: str
    created_at: datetime.datetime
    predicted_class: Optional[str] = None
    confidence: Optional[float] = None
    explanation: Optional[str] = None

    class Config:
        from_attributes = True

class IncidentCreate(BaseModel):
    title: Optional[str] = "Cyberbullying Incident"
    platform: Optional[str] = "Social Media"

class IncidentResponse(BaseModel):
    id: int
    incident_code: str
    user_id: int
    title: str
    platform: str
    status: str
    primary_category: Optional[str] = None
    confidence: float
    severity: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    evidence_count: int = 0
    evidence_items: Optional[List[EvidenceItemResponse]] = []

    class Config:
        from_attributes = True
