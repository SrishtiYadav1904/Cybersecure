import datetime
import uuid
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
)
from sqlalchemy.orm import relationship
from backend.app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=generate_uuid, unique=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="USER", nullable=False) # USER, ADMIN, CONSULTANT
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incidents = relationship("Incident", back_populates="user", cascade="all, delete-orphan")
    support_sessions = relationship("SupportSession", back_populates="user")
    help_requests = relationship("HelpRequest", back_populates="user")

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. CB-2026-000001
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), default="Cyberbullying Incident")
    platform = Column(String(100), default="Unknown") # Instagram, WhatsApp, Twitter, etc.
    status = Column(String(50), default="ACTIVE") # ACTIVE, REPORTED, PENDING_REVIEW, RESOLVED
    primary_category = Column(String(100), nullable=True)
    confidence = Column(Float, default=0.0)
    severity = Column(String(50), default="MODERATE") # LOW, MODERATE, HIGH, SEVERE
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="incidents")
    evidence_items = relationship("Evidence", back_populates="incident", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="incident", cascade="all, delete-orphan")
    help_requests = relationship("HelpRequest", back_populates="incident")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False)
    evidence_type = Column(String(50), nullable=False) # SCREENSHOT, CHAT, TEXT
    file_path = Column(String(500), nullable=True)
    ocr_raw_text = Column(Text, nullable=True)
    edited_text = Column(Text, nullable=False)
    detected_language = Column(String(50), default="English")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="evidence_items")
    messages = relationship("Message", back_populates="evidence", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="evidence", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer, ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False)
    sender_name = Column(String(100), default="Unknown")
    message_text = Column(Text, nullable=False)
    timestamp_str = Column(String(50), nullable=True)
    is_targeted = Column(Boolean, default=False)
    predicted_category = Column(String(100), nullable=True)
    confidence = Column(Float, default=0.0)

    evidence = relationship("Evidence", back_populates="messages")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer, ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False)
    predicted_class = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    probabilities_json = Column(JSON, nullable=True) # Full class probability distribution
    explainability_json = Column(JSON, nullable=True) # Token attributions & reasoning
    important_tokens_json = Column(JSON, nullable=True) # Identified salient offensive terms
    model_version = Column(String(50), default="CB-EXP-002")
    dataset_version = Column(String(50), default="CB-DATA-002", nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    evidence = relationship("Evidence", back_populates="predictions")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    report_code = Column(String(50), unique=True, index=True, nullable=False) # REP-2026-000001
    pdf_path = Column(String(500), nullable=False)
    summary_json = Column(JSON, nullable=True)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    incident = relationship("Incident", back_populates="reports")

class SupportSession(Base):
    __tablename__ = "support_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True)
    session_summary = Column(Text, nullable=True)
    wellbeing_indicators_json = Column(JSON, nullable=True) # stress_level, emotional_valence, urgency
    escalation_level = Column(String(50), default="NORMAL") # NORMAL, ELEVATED, URGENT_ESCALATION
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="support_sessions")
    messages = relationship("SupportMessage", back_populates="session", cascade="all, delete-orphan")

class SupportMessage(Base):
    __tablename__ = "support_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("support_sessions.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(50), nullable=False) # user, assistant, consultant
    content = Column(Text, nullable=False)
    rag_sources_json = Column(JSON, nullable=True)
    wellbeing_signals_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("SupportSession", back_populates="messages")

class HelpRequest(Base):
    __tablename__ = "help_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_code = Column(String(50), unique=True, index=True, nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    account_username = Column(String(100), nullable=True)
    platform = Column(String(100), nullable=False)
    num_bullies = Column(Integer, default=1)
    bully_accounts_json = Column(JSON, nullable=True) # List of bully handles / links
    whatsapp_details_json = Column(JSON, nullable=True) # group name, numbers if whatsapp
    additional_notes = Column(Text, nullable=True)
    status = Column(String(50), default="NEW") # NEW, IN_REVIEW, CONTACTED, ESCALATED, RESOLVED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="help_requests")
    incident = relationship("Incident", back_populates="help_requests")

class SlangTerm(Base):
    __tablename__ = "slang_terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(100), unique=True, index=True, nullable=False)
    language = Column(String(50), default="Hinglish")
    candidate_meaning = Column(String(255), nullable=True)
    frequency = Column(Integer, default=1)
    status = Column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED
    sample_context = Column(Text, nullable=True)
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)

class DriftEvent(Base):
    __tablename__ = "drift_events"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False) # e.g. PSI, KS_TEST, OOV_RATE
    metric_value = Column(Float, nullable=False)
    drift_status = Column(String(50), nullable=False) # STABLE, WARNING, DRIFT_DETECTED
    affected_classes_json = Column(JSON, nullable=True)
    sample_size = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False) # CYBERCRIME, HELPLINE, WOMEN_SAFETY, PLATFORM
    name = Column(String(255), nullable=False)
    contact_number = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_emergency = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    version_tag = Column(String(50), unique=True, index=True, nullable=False) # CB-RO-001
    model_name = Column(String(150), nullable=False)
    training_date = Column(DateTime, default=datetime.datetime.utcnow)
    dataset_version = Column(String(100), default="unified_v1.0")
    features_description = Column(String(255), default="PCA(GloVe 100d -> 30d) + Contextual Transformer + Stacking AML")
    macro_f1 = Column(Float, default=0.0)
    pr_auc = Column(Float, default=0.0)
    accuracy = Column(Float, default=0.0)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
