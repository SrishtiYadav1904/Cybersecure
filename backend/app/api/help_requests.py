import uuid
import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.database.models import User, Incident, HelpRequest
from backend.app.auth.dependencies import get_current_user, require_consultant
from backend.app.schemas.support import HelpRequestCreate, HelpRequestResponse

router = APIRouter(prefix="/help-request", tags=["Help Requests & Consultant Escalation"])

@router.post("", response_model=HelpRequestResponse, status_code=status.HTTP_201_CREATED)
def submit_help_request(
    payload: HelpRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits a structured help request for human consultant escalation:
    - Captures user contact details
    - Dynamically catalogs offending bully handles & links
    - Stores platform-specific parameters (e.g. WhatsApp group names/phone numbers)
    - Updates attached incident status to 'PENDING_REVIEW'
    """
    req_code = f"HLP-{datetime.datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"

    # Build bully accounts JSON
    bully_list = [acc.dict() for acc in payload.bully_accounts]
    whatsapp_info = None
    if payload.platform.lower() == "whatsapp":
        whatsapp_info = {
            "group_name": payload.whatsapp_group_name,
            "numbers": payload.whatsapp_numbers or []
        }

    help_req = HelpRequest(
        request_code=req_code,
        incident_id=payload.incident_id,
        user_id=current_user.id,
        full_name=payload.full_name,
        age=payload.age,
        email=payload.email,
        phone=payload.phone,
        account_username=payload.account_username,
        platform=payload.platform,
        num_bullies=payload.num_bullies,
        bully_accounts_json=bully_list,
        whatsapp_details_json=whatsapp_info,
        additional_notes=payload.additional_notes,
        status="NEW"
    )
    db.add(help_req)

    # Link incident if provided
    if payload.incident_id:
        incident = db.query(Incident).filter(Incident.id == payload.incident_id).first()
        if incident:
            incident.status = "PENDING_REVIEW"

    db.commit()
    db.refresh(help_req)

    return HelpRequestResponse(
        id=help_req.id,
        request_code=help_req.request_code,
        incident_id=help_req.incident_id,
        user_id=help_req.user_id,
        full_name=help_req.full_name,
        email=help_req.email,
        platform=help_req.platform,
        num_bullies=help_req.num_bullies,
        status=help_req.status,
        created_at=help_req.created_at
    )

@router.get("/cases", response_model=List[HelpRequestResponse])
def get_escalated_cases(
    current_user: User = Depends(require_consultant),
    db: Session = Depends(get_db)
):
    """
    Consultant Portal: View all escalated help requests, active cases, and triage statuses.
    Requires role CONSULTANT.
    """
    cases = db.query(HelpRequest).order_by(HelpRequest.created_at.desc()).all()
    return [
        HelpRequestResponse(
            id=c.id,
            request_code=c.request_code,
            incident_id=c.incident_id,
            user_id=c.user_id,
            full_name=c.full_name,
            email=c.email,
            platform=c.platform,
            num_bullies=c.num_bullies,
            status=c.status,
            created_at=c.created_at
        )
        for c in cases
    ]
