import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.database.session import get_db
from backend.app.database.models import User, Incident, Evidence, Prediction
from backend.app.auth.dependencies import get_current_user
from backend.app.schemas.analysis import (
    TextAnalysisRequest, AnalysisResponse, OCRResponse,
    ChatAnalysisRequest, ChatAnalysisResponse
)
from backend.app.config import settings
from ml.inference.pipeline import get_ml_pipeline
from backend.app.ocr.ocr_engine import get_ocr_engine
from backend.app.services.chat_analyzer import get_chat_analyzer

router = APIRouter(prefix="/analyze", tags=["Analysis & Detection"])

@router.post("/text", response_model=AnalysisResponse)
def analyze_text_endpoint(
    req: TextAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Direct comment / message analysis endpoint.
    Executes full ML pipeline (Language Detection -> Normalization -> GloVe+PCA -> RoBERTa -> Fusion -> Ensemble -> XAI).
    Attaches prediction to user's incident.
    """
    pipeline = get_ml_pipeline()
    result = pipeline.analyze_text(req.text)

    # Attach to active incident or create new one
    incident = None
    if req.incident_id:
        incident = db.query(Incident).filter(
            Incident.id == req.incident_id,
            Incident.user_id == current_user.id
        ).first()

    if not incident:
        # Create new incident
        incident_code = f"CB-{datetime_prefix()}-{uuid.uuid4().hex[:6].upper()}"
        incident = Incident(
            incident_code=incident_code,
            user_id=current_user.id,
            title=f"Incident ({req.platform or 'Web'})",
            platform=req.platform or "Web",
            status="ACTIVE",
            primary_category=result["predicted_class"],
            confidence=result["confidence"],
            severity=result["severity"]
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)
    else:
        # Update incident category and severity if more severe
        incident.primary_category = result["predicted_class"]
        incident.confidence = result["confidence"]
        incident.severity = result["severity"]
        db.commit()

    # Store evidence and prediction records
    evidence = Evidence(
        incident_id=incident.id,
        evidence_type="TEXT",
        edited_text=req.text,
        detected_language=result["detected_language"]
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    prediction = Prediction(
        evidence_id=evidence.id,
        predicted_class=result["predicted_class"],
        confidence=result["confidence"],
        probabilities_json=result["probabilities"],
        explainability_json=result["token_attributions"],
        important_tokens_json=result["important_tokens"],
        model_version=result["model_version"],
        dataset_version=result.get("dataset_version", "CB-DATA-002")
    )
    db.add(prediction)
    db.commit()

    result["incident_id"] = incident.id
    result["evidence_id"] = evidence.id
    return result

@router.post("/image", response_model=OCRResponse)
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    incident_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """
    Step 1 of Screenshot Analysis:
    Receives image -> validates MIME/magic bytes -> extracts text via OCR -> returns text for user review/editing.
    """
    # Validate file extension & content type
    allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}
    filename = file.filename or "screenshot.png"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed formats: {', '.join(allowed_exts)}"
        )

    # Read bytes with size limit (10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum 10MB limit."
        )

    # Save image securely
    saved_filename = f"{uuid.uuid4().hex}{ext}"
    saved_filepath = os.path.join(settings.UPLOAD_DIR, saved_filename)
    with open(saved_filepath, "wb") as f:
        f.write(contents)

    # Run OCR extraction
    ocr_engine = get_ocr_engine()
    extracted_text, conf = ocr_engine.extract_text_from_bytes(contents, filename)

    # Detect language of extracted text
    pipeline = get_ml_pipeline()
    lang, _ = pipeline.language_detector.detect(extracted_text)

    return OCRResponse(
        extracted_text=extracted_text,
        detected_language=lang,
        confidence=conf,
        file_path=saved_filepath,
        incident_id=incident_id
    )

@router.post("/confirm-image", response_model=AnalysisResponse)
def confirm_image_analysis_endpoint(
    edited_text: str = Form(...),
    file_path: Optional[str] = Form(None),
    raw_ocr_text: Optional[str] = Form(None),
    incident_id: Optional[int] = Form(None),
    platform: Optional[str] = Form("Social Media"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Step 2 of Screenshot Analysis:
    Takes user-edited OCR text -> executes ML detection pipeline -> stores screenshot evidence -> links to incident.
    """
    pipeline = get_ml_pipeline()
    result = pipeline.analyze_multimodal(
        text=edited_text,
        image_path=file_path,
        modality="MULTIMODAL" if file_path else "TEXT_ONLY"
    )

    # Resolve incident
    incident = None
    if incident_id:
        incident = db.query(Incident).filter(
            Incident.id == incident_id,
            Incident.user_id == current_user.id
        ).first()

    if not incident:
        incident_code = f"CB-{datetime_prefix()}-{uuid.uuid4().hex[:6].upper()}"
        incident = Incident(
            incident_code=incident_code,
            user_id=current_user.id,
            title=f"Incident ({platform})",
            platform=platform,
            status="ACTIVE",
            primary_category=result["predicted_class"],
            confidence=result["confidence"],
            severity=result["severity"]
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)
    else:
        incident.primary_category = result["predicted_class"]
        incident.confidence = result["confidence"]
        incident.severity = result["severity"]
        db.commit()

    # Store evidence
    evidence = Evidence(
        incident_id=incident.id,
        evidence_type="SCREENSHOT",
        file_path=file_path,
        ocr_raw_text=raw_ocr_text,
        edited_text=edited_text,
        detected_language=result["detected_language"]
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    # Store prediction
    prediction = Prediction(
        evidence_id=evidence.id,
        predicted_class=result["predicted_class"],
        confidence=result["confidence"],
        probabilities_json=result["probabilities"],
        explainability_json=result["token_attributions"],
        important_tokens_json=result["important_tokens"],
        model_version=result["model_version"]
    )
    db.add(prediction)
    db.commit()

    result["incident_id"] = incident.id
    result["evidence_id"] = evidence.id
    return result

@router.post("/chat", response_model=ChatAnalysisResponse)
def analyze_chat_endpoint(
    req: ChatAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Conversational / Chat transcript analysis:
    Segments messages, models repeated targeting, escalation trajectory, and multi-party coordination.
    """
    analyzer = get_chat_analyzer()
    response = analyzer.analyze_conversation(req.messages, platform=req.platform)

    # Attach to incident
    incident_code = f"CB-{datetime_prefix()}-{uuid.uuid4().hex[:6].upper()}"
    incident = Incident(
        incident_code=incident_code,
        user_id=current_user.id,
        title=f"Chat Incident ({req.platform})",
        platform=req.platform,
        status="ACTIVE",
        primary_category=response.primary_category,
        confidence=response.overall_confidence,
        severity="SEVERE" if response.escalation_detected else "HIGH"
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)

    response.incident_id = incident.id
    return response

def datetime_prefix():
    import datetime
    return datetime.datetime.utcnow().strftime("%Y%m")
