import uuid
import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.database.models import User, Incident, Evidence, Prediction, Report
from backend.app.auth.dependencies import get_current_user
from backend.app.schemas.incident import IncidentCreate, IncidentResponse, EvidenceItemResponse
from backend.app.reports.report_generator import get_report_generator

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=List[IncidentResponse])
def list_incidents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all incidents belonging to the authenticated user (or all if admin)."""
    if current_user.role == "ADMIN":
        incidents = db.query(Incident).order_by(Incident.created_at.desc()).all()
    else:
        incidents = db.query(Incident).filter(Incident.user_id == current_user.id).order_by(Incident.created_at.desc()).all()

    results = []
    for inc in incidents:
        count = db.query(Evidence).filter(Evidence.incident_id == inc.id).count()
        results.append(IncidentResponse(
            id=inc.id,
            incident_code=inc.incident_code,
            user_id=inc.user_id,
            title=inc.title,
            platform=inc.platform,
            status=inc.status,
            primary_category=inc.primary_category,
            confidence=inc.confidence,
            severity=inc.severity,
            created_at=inc.created_at,
            updated_at=inc.updated_at,
            evidence_count=count
        ))
    return results

@router.post("", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(
    req: IncidentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new active incident."""
    month_prefix = datetime.datetime.utcnow().strftime("%Y%m")
    incident_code = f"CB-{month_prefix}-{uuid.uuid4().hex[:6].upper()}"

    incident = Incident(
        incident_code=incident_code,
        user_id=current_user.id,
        title=req.title or "Cyberbullying Incident",
        platform=req.platform or "Social Media",
        status="ACTIVE",
        severity="LOW"
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)

    return IncidentResponse(
        id=incident.id,
        incident_code=incident.incident_code,
        user_id=incident.user_id,
        title=incident.title,
        platform=incident.platform,
        status=incident.status,
        primary_category=incident.primary_category,
        confidence=incident.confidence,
        severity=incident.severity,
        created_at=incident.created_at,
        updated_at=incident.updated_at,
        evidence_count=0,
        evidence_items=[]
    )

@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch complete incident details, including evidence timeline and predictions."""
    query = db.query(Incident).filter(Incident.id == incident_id)
    if current_user.role != "ADMIN":
        query = query.filter(Incident.user_id == current_user.id)
    
    incident = query.first()
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )

    evidence_records = db.query(Evidence).filter(Evidence.incident_id == incident.id).order_by(Evidence.created_at.asc()).all()
    evidence_items = []
    for ev in evidence_records:
        pred = db.query(Prediction).filter(Prediction.evidence_id == ev.id).first()
        pred_class = pred.predicted_class if pred else None
        pred_conf = pred.confidence if pred else None
        pred_expl = pred.explainability_json if pred else None

        evidence_items.append(EvidenceItemResponse(
            id=ev.id,
            evidence_type=ev.evidence_type,
            file_path=ev.file_path,
            ocr_raw_text=ev.ocr_raw_text,
            edited_text=ev.edited_text,
            detected_language=ev.detected_language,
            created_at=ev.created_at,
            predicted_class=pred_class,
            confidence=pred_conf,
            explanation=str(pred_expl) if pred_expl else None
        ))

    return IncidentResponse(
        id=incident.id,
        incident_code=incident.incident_code,
        user_id=incident.user_id,
        title=incident.title,
        platform=incident.platform,
        status=incident.status,
        primary_category=incident.primary_category,
        confidence=incident.confidence,
        severity=incident.severity,
        created_at=incident.created_at,
        updated_at=incident.updated_at,
        evidence_count=len(evidence_items),
        evidence_items=evidence_items
    )

@router.post("/{incident_id}/close")
def close_incident_and_generate_report(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    User Decision 'STOP':
    Concludes evidence collection, transitions status to 'REPORTED', and compiles the official PDF report artifact.
    """
    query = db.query(Incident).filter(Incident.id == incident_id)
    if current_user.role != "ADMIN":
        query = query.filter(Incident.user_id == current_user.id)
    incident = query.first()

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )

    incident.status = "REPORTED"
    db.commit()

    # Compile data for PDF generator
    evidence_records = db.query(Evidence).filter(Evidence.incident_id == incident.id).all()
    evidence_payload = []
    for ev in evidence_records:
        pred = db.query(Prediction).filter(Prediction.evidence_id == ev.id).first()
        evidence_payload.append({
            "evidence_type": ev.evidence_type,
            "detected_language": ev.detected_language,
            "edited_text": ev.edited_text,
            "predicted_class": pred.predicted_class if pred else "Unclassified",
            "confidence": pred.confidence if pred else 0.0,
            "explanation": pred.explainability_json if pred else "Evidence cataloged."
        })

    pdf_data = {
        "incident_code": incident.incident_code,
        "platform": incident.platform,
        "primary_category": incident.primary_category or "Cyberbullying",
        "confidence": incident.confidence,
        "severity": incident.severity,
        "created_at": incident.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "evidence_items": evidence_payload
    }

    report_gen = get_report_generator()
    pdf_path = report_gen.generate_pdf(pdf_data)

    # Save report record in database
    report_code = f"REP-{incident.incident_code.replace('CB-', '')}"
    existing_rep = db.query(Report).filter(Report.incident_id == incident.id).first()
    if existing_rep:
        existing_rep.pdf_path = pdf_path
        db.commit()
        report_record = existing_rep
    else:
        report_record = Report(
            incident_id=incident.id,
            user_id=current_user.id,
            report_code=report_code,
            pdf_path=pdf_path,
            summary_json=pdf_data
        )
        db.add(report_record)
        db.commit()
        db.refresh(report_record)

    return {
        "status": "success",
        "message": "Incident concluded. Forensic report generated successfully.",
        "incident_code": incident.incident_code,
        "report_id": report_record.id,
        "report_code": report_record.report_code,
        "download_url": f"/api/reports/{report_record.id}/download"
    }
