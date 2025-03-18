from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set!")

# Parsing URL dari format mysql:// ke dictionary
parsed_url = urlparse(DATABASE_URL)

db_config = {
    "user": parsed_url.username,
    "password": parsed_url.password,
    "host": parsed_url.hostname,
    "port": parsed_url.port,
    "database": parsed_url.path[1:]  # Hapus "/" di depan nama database
}

engine = create_engine(**db_config)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
  __tablename__ = 'urls'

  id = Column(Integer, primary_key=True, index=True)
  original_url = Column(String(500), nullable=False)
  short_url = Column(String(20), unique=True, nullable=False)
  click_count = Column(Integer, default=0)
  created_at = Column(DateTime, default=datetime.utcnow)
  expires_at = Column(DateTime, nullable=True)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()