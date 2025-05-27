from pydantic import BaseModel
from typing import Optional


class EmailRequest(BaseModel):
    subject: str
    body: str
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
