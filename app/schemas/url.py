from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class URLRequest(BaseModel):
    original_url: str
    expire_in_days: int = 7
    custom_slug: Optional[str] = None
    password: Optional[str] = None


class URLResponse(BaseModel):
    id: int
    short_url: str
    original_url: str
    expires_at: datetime

    class Config:
        from_attributes: True


@field_validator("expire_in_days")
def expire_in_days_must_be_between_0_and_8(cls, v):
    if v < 0 or v >= 8:
        raise ValueError("expire_in_days must be between 1 and 7")
    return v
