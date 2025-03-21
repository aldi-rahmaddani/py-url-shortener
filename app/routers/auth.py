from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.db import Base, get_db 
from app.models.user import User
from app.schemas.user import RegisterRequest
from app.utils.authentication import hash_password, verify_password, create_access_token

from datetime import timedelta
import os

router = APIRouter()

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

  return {"message": "Registration successful"}

token_expires_in_hours = os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")

@router.post("/login")
def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
  user = db.query(User).filter(User.email == form_data.username).first()
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(status_code=400, detail="Invalid email or password")
  
  access_token = create_access_token({"sub": user.email}, timedelta(hours=float(token_expires_in_hours)))
  return {"access_token": access_token, "token_type": "bearier"}
