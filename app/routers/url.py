from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random, string

from app.models.base import Base, get_db
from app.models.url import URL
from app.models.user import User
from app.schemas.url import URLRequest, URLResponse

from app.utils.authentication import get_current_user

router = APIRouter()

def generate_short_url():
  return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@router.get("/list", response_model=list[URLResponse])
def get_list_url(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  """Mengambil semua URL milik user yang sedang login"""
  urls = db.query(URL).filter(URL.user_id == current_user.id).all()
    
  if not urls:
    raise HTTPException(status_code=404, detail="No URLs found for this user")
    
  return urls

@router.get("/{short_url}")
def redirect_to_original(short_url: str, db: Session = Depends(get_db)):
  url_entry = db.query(URL).filter(URL.short_url == short_url).first()

  if not url_entry:
    raise HTTPException(status_code=404, detail="Short URL not found")

  if url_entry.expires_at and datetime.utcnow() > url_entry.expires_at:
    raise HTTPException(status_code=410, detail="Short URL has expired")

  url_entry.click_count += 1
  db.commit()

  return RedirectResponse(url_entry.original_url)

@router.post("/", response_model=URLResponse)
def shorten_url(request: URLRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  short_url = ''

  # Ensure uniqueness
  if request.custom_slug:
    existing_url = db.query(URL).filter(URL.short_url == request.custom_slug).first()

    if existing_url:
      raise HTTPException(status_code=400, detail="Custom slug already in use")

    short_url = request.custom_slug
  else:
    short_url = generate_short_url()

    while db.query(URL).filter(URL.short_url == short_url).first():
      short_url = generate_short_url()

  expires_at = datetime.utcnow() + timedelta(days=request.expire_in_days)
  new_url = URL(original_url=request.original_url, short_url=short_url, expires_at=expires_at, user_id=current_user.id)

  db.add(new_url)
  db.commit()
  db.refresh(new_url)

  return new_url


