from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.config.db import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100))
  email = Column(String(100), unique=True, index=True, nullable=False)
  hashed_password = Column(String(100), nullable=False)
  url_limit = Column(Integer, default=10)

  urls = relationship("URL", back_populates="owner")  # Relasi ke URL