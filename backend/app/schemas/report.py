from typing import Optional, Dict, Any
from pydantic import BaseModel
import datetime

class ReportResponse(BaseModel):
    id: int
    incident_id: int
    user_id: int
    report_code: str
    pdf_path: str
    summary_json: Optional[Dict[str, Any]] = None
    generated_at: datetime.datetime
    download_url: str

    class Config:
        from_attributes = True
