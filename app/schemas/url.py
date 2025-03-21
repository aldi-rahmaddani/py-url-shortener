from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional

class URLRequest(BaseModel):
  original_url: str
  expire_in_days: conint(gt=0, lt=8) = 7
  custom_slug: Optional[str] = None

class URLResponse(BaseModel):
  id: int
  short_url: str
  original_url: str
  expires_at: datetime

  class Config:
    from_attributes: True
  
