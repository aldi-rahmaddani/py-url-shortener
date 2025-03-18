from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl, conint
import random
import string
from datetime import datetime, timedelta

from database import get_db
from database import URL, User
from utils import hash_password

router = APIRouter()

def generate_short_url():
  return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class URLRequest(BaseModel):
  original_url: str
  expire_in_days: conint(gt=0, lt=8) = 7
  custom_slug: str | None = None

@router.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
  short_url = ''

  if request.custom_slug:
    # Cek apakah short_url sudah ada di database
    existing_url = db.query(URL).filter(URL.short_url == request.custom_slug).first()
    if existing_url:
      raise HTTPException(status_code=400, detail="Custom slug already in use")
    short_url = request.custom_slug
  else:
    short_url = generate_short_url()

    # Cek apakah short_url sudah ada di database
    while db.query(URL).filter(URL.short_url == short_url).first():
      short_url = generate_short_url()

  expires_at = datetime.utcnow() + timedelta(days=request.expire_in_days)

  new_url = URL(original_url=request.original_url, short_url=short_url, expires_at=expires_at)
  db.add(new_url)
  db.commit()
  db.refresh(new_url)

  return {"short_url": short_url, "original_url": request.original_url, "expires_at": expires_at.strftime("%Y-%m-%d %H:%M:%S")}

@router.get("/shorten/{short_url}")
def redirect_to_original(short_url: str, db: Session = Depends(get_db)):
  url_entry = db.query(URL).filter(URL.short_url == short_url).first()

  if url_entry is None:
    raise HTTPException(status_code=404, detail="Short URL not found")
  
  # Cek apakah URL sudah expired
  if url_entry.expires_at and datetime.utcnow() > url_entry.expires_at:
    raise HTTPException(status_code=410, detail="Short URL has expired")
  
  url_entry.click_count += 1
  db.commit()

  return RedirectResponse(url_entry.original_url)

@router.get("/urls")
def get_all_urls(db:Session = Depends(get_db)):
  urls = db.query(URL).all()
  return urls

class RegisterRequest(BaseModel):
  name: str
  email: str
  password: str

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
  existing_user = db.query(User).filter(User.email == request.email).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="Email is already registered")
    
  hashed_password = hash_password(request.password)
  new_user = User(name=request.name, email=request.email, hashed_password=hashed_password)
    
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return {"message": "Registrasi berhasil"}