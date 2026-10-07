from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import datetime

class TextAnalysisRequest(BaseModel):
    text: str
    incident_id: Optional[int] = None
    platform: Optional[str] = "Web"

class TokenAttribution(BaseModel):
    token: str
    weight: float
    is_offensive: bool

class ClassProbability(BaseModel):
    category: str
    probability: float

class AnalysisResponse(BaseModel):
    predicted_class: str
    confidence: float
    is_cyberbullying: bool
    severity: str # LOW, MODERATE, HIGH, SEVERE
    detected_language: str
    normalized_text: str
    probabilities: List[ClassProbability]
    important_tokens: List[str]
    token_attributions: List[TokenAttribution]
    explanation: str
    recommended_action: str
    model_version: str
    incident_id: Optional[int] = None
    evidence_id: Optional[int] = None
    model_config = {"protected_namespaces": ()}

class OCRResponse(BaseModel):
    extracted_text: str
    detected_language: str
    confidence: float
    file_path: Optional[str] = None
    incident_id: Optional[int] = None

class ChatMessageInput(BaseModel):
    sender: str
    text: str
    timestamp: Optional[str] = None

class ChatAnalysisRequest(BaseModel):
    messages: List[ChatMessageInput]
    platform: Optional[str] = "Chat"
    incident_id: Optional[int] = None

class AnalyzedChatMessage(BaseModel):
    sender: str
    text: str
    timestamp: Optional[str] = None
    predicted_class: str
    confidence: float
    is_bullying: bool

class ChatAnalysisResponse(BaseModel):
    total_messages: int
    analyzed_messages: List[AnalyzedChatMessage]
    primary_category: str
    overall_confidence: float
    repeated_targeting_detected: bool
    repeated_targeting_summary: str
    active_bullies: List[str]
    escalation_detected: bool
    incident_assessment: str
    recommended_safety_action: str
    incident_id: Optional[int] = None
