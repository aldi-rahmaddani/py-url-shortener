from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class URL(Base):
  __tablename__ = "urls"

  id = Column(Integer, primary_key=True, index=True)
  original_url = Column(String(500), nullable=False)
  short_url = Column(String(20), unique=True, nullable=False)
  click_count = Column(Integer, default=0)
  created_at = Column(DateTime, default=datetime.utcnow)
  expires_at = Column(DateTime)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

  owner = relationship("User", back_populates="urls")  # Relasi ke User
