from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
import datetime

class SupportMessageSend(BaseModel):
    session_id: Optional[int] = None
    incident_id: Optional[int] = None
    message: str

class SupportMessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    rag_sources: Optional[List[Any]] = None
    wellbeing_signals: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class SupportSessionResponse(BaseModel):
    id: int
    user_id: int
    incident_id: Optional[int] = None
    session_summary: Optional[str] = None
    wellbeing_indicators: Optional[Dict[str, Any]] = None
    escalation_level: str
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    messages: List[SupportMessageResponse] = []

    class Config:
        from_attributes = True

class BullyAccount(BaseModel):
    handle: str
    profile_url: Optional[str] = None
    platform: Optional[str] = None

class HelpRequestCreate(BaseModel):
    incident_id: Optional[int] = None
    full_name: str
    age: Optional[int] = None
    email: EmailStr
    phone: Optional[str] = None
    account_username: Optional[str] = None
    platform: str
    num_bullies: int = 1
    bully_accounts: List[BullyAccount] = []
    whatsapp_group_name: Optional[str] = None
    whatsapp_numbers: Optional[List[str]] = None
    additional_notes: Optional[str] = None

class HelpRequestResponse(BaseModel):
    id: int
    request_code: str
    incident_id: Optional[int] = None
    user_id: int
    full_name: str
    email: str
    platform: str
    num_bullies: int
    status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class ResourceResponse(BaseModel):
    id: int
    category: str
    name: str
    contact_number: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    is_emergency: bool

    class Config:
        from_attributes = True
