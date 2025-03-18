from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100))
  email = Column(String(100), unique=True, index=True, nullable=False)
  hashed_password = Column(String(100), nullable=False)
  url_limit = Column(Integer, default=10)

  urls = relationship("URL", back_populates="owner")  # Relasi ke URL

class URL(Base):
  __tablename__ = 'urls'

  id = Column(Integer, primary_key=True, index=True)
  original_url = Column(String(500), nullable=False)
  short_url = Column(String(20), unique=True, nullable=False)
  click_count = Column(Integer, default=0)
  created_at = Column(DateTime, default=datetime.utcnow)
  expires_at = Column(DateTime, nullable=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

  owner = relationship("User", back_populates="urls")  # Relasi ke User

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()