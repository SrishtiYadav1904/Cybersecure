import os
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.config import settings

from backend.app.database.session import get_db
from backend.app.database.models import User, Incident, SupportSession, SupportMessage, Resource
from backend.app.auth.dependencies import get_current_user
from backend.app.schemas.support import (
    SupportMessageSend, SupportMessageResponse, SupportSessionResponse, ResourceResponse
)
from backend.app.support.support_agent import get_support_agent

router = APIRouter(prefix="/support", tags=["Support AI & Wellbeing"])

@router.post("/start", response_model=SupportSessionResponse)
def start_support_session(
    incident_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initializes a new support session or retrieves current active session.
    Retrieves previous incident summary and past session indicators for continuity.
    """
    # Look for existing active session
    active_session = db.query(SupportSession).filter(
        SupportSession.user_id == current_user.id,
        SupportSession.is_active == True
    ).order_by(SupportSession.created_at.desc()).first()

    if not active_session:
        active_session = SupportSession(
            user_id=current_user.id,
            incident_id=incident_id,
            escalation_level="NORMAL",
            is_active=True
        )
        db.add(active_session)
        db.commit()
        db.refresh(active_session)

        # Post initial welcoming guidance message
        welcome_text = (
            f"Hello {current_user.full_name or current_user.username}. I am your CyberGuard Support Assistant. "
            "I'm here to provide practical digital safety guidance, evidence preservation steps, and official platform advice. "
            "Please note that I do not provide psychiatric diagnoses. How are you holding up today?"
        )
        welcome_msg = SupportMessage(
            session_id=active_session.id,
            sender="assistant",
            content=welcome_text
        )
        db.add(welcome_msg)
        db.commit()

    messages = db.query(SupportMessage).filter(
        SupportMessage.session_id == active_session.id
    ).order_by(SupportMessage.created_at.asc()).all()

    return SupportSessionResponse(
        id=active_session.id,
        user_id=active_session.user_id,
        incident_id=active_session.incident_id,
        session_summary=active_session.session_summary,
        wellbeing_indicators=active_session.wellbeing_indicators_json,
        escalation_level=active_session.escalation_level,
        is_active=active_session.is_active,
        created_at=active_session.created_at,
        updated_at=active_session.updated_at,
        messages=[
            SupportMessageResponse(
                id=m.id,
                sender=m.sender,
                content=m.content,
                rag_sources=m.rag_sources_json,
                wellbeing_signals=m.wellbeing_signals_json,
                created_at=m.created_at
            )
            for m in messages
        ]
    )

@router.post("/message", response_model=SupportMessageResponse)
def send_support_message(
    payload: SupportMessageSend,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits user message to the grounded Support Assistant:
    1. Saves user message
    2. Runs intent detection & RAG retrieval against official knowledge base
    3. Evaluates wellbeing and stress indicators
    4. Enforces safety guardrails (no psychiatric diagnosis)
    5. Saves and returns assistant response
    """
    session = None
    if payload.session_id:
        session = db.query(SupportSession).filter(
            SupportSession.id == payload.session_id,
            SupportSession.user_id == current_user.id
        ).first()

    if not session:
        session = db.query(SupportSession).filter(
            SupportSession.user_id == current_user.id,
            SupportSession.is_active == True
        ).order_by(SupportSession.created_at.desc()).first()

    if not session:
        session = SupportSession(
            user_id=current_user.id,
            incident_id=payload.incident_id,
            is_active=True
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = SupportMessage(
        session_id=session.id,
        sender="user",
        content=payload.message
    )
    db.add(user_msg)
    db.commit()

    # Retrieve incident summary if attached
    incident_summary = None
    if session.incident_id:
        inc = db.query(Incident).filter(Incident.id == session.incident_id).first()
        if inc:
            incident_summary = {
                "incident_code": inc.incident_code,
                "primary_category": inc.primary_category,
                "confidence": inc.confidence,
                "platform": inc.platform
            }

    # Generate grounded AI response
    agent = get_support_agent()
    agent_resp = agent.generate_response(
        user_message=payload.message,
        incident_context=incident_summary
    )
    resp_text = agent_resp.get("response", "")
    rag_sources = agent_resp.get("rag_sources", [])
    indicators = agent_resp.get("wellbeing_indicators", {})

    # Update session wellbeing metrics
    session.wellbeing_indicators_json = indicators
    session.escalation_level = indicators.get("escalation_urgency", "NORMAL")
    db.commit()

    # Save assistant response
    assistant_msg = SupportMessage(
        session_id=session.id,
        sender="assistant",
        content=resp_text,
        rag_sources_json=rag_sources,
        wellbeing_signals_json=indicators
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return SupportMessageResponse(
        id=assistant_msg.id,
        sender=assistant_msg.sender,
        content=assistant_msg.content,
        rag_sources=rag_sources,
        wellbeing_signals=indicators,
        created_at=assistant_msg.created_at
    )

@router.get("/history", response_model=List[SupportSessionResponse])
def get_support_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve past support session summaries for daily follow-up tracking."""
    sessions = db.query(SupportSession).filter(
        SupportSession.user_id == current_user.id
    ).order_by(SupportSession.created_at.desc()).all()

    results = []
    for s in sessions:
        msgs = db.query(SupportMessage).filter(
            SupportMessage.session_id == s.id
        ).order_by(SupportMessage.created_at.asc()).all()

        results.append(SupportSessionResponse(
            id=s.id,
            user_id=s.user_id,
            incident_id=s.incident_id,
            session_summary=s.session_summary or "Support session recorded.",
            wellbeing_indicators=s.wellbeing_indicators_json,
            escalation_level=s.escalation_level,
            is_active=s.is_active,
            created_at=s.created_at,
            updated_at=s.updated_at,
            messages=[
                SupportMessageResponse(
                    id=m.id,
                    sender=m.sender,
                    content=m.content,
                    rag_sources=m.rag_sources_json,
                    wellbeing_signals=m.wellbeing_signals_json,
                    created_at=m.created_at
                )
                for m in msgs
            ]
        ))
    return results

@router.get("/resources", response_model=List[ResourceResponse])
def get_emergency_resources(db: Session = Depends(get_db)):
    """Retrieve official configurable cybercrime, police, and wellbeing emergency numbers."""
    resources = db.query(Resource).filter(Resource.is_active == True).all()
    if not resources:
        # Load from helplines.json if table not yet seeded
        kb_file = os.path.join(settings.KNOWLEDGE_BASE_DIR, "emergency_resources", "helplines.json")
        if os.path.exists(kb_file):
            with open(kb_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [
                    ResourceResponse(
                        id=i+1,
                        category=d["category"],
                        name=d["name"],
                        contact_number=d.get("contact_number"),
                        website=d.get("website"),
                        description=d.get("description"),
                        is_emergency=d.get("is_emergency", False)
                    )
                    for i, d in enumerate(data)
                ]
    return [
        ResourceResponse(
            id=r.id,
            category=r.category,
            name=r.name,
            contact_number=r.contact_number,
            website=r.website,
            description=r.description,
            is_emergency=r.is_emergency
        )
        for r in resources
    ]
