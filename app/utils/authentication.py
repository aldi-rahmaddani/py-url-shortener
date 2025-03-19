from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.user import User
import os
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: 
  return pwd_context.verify(plain_password, hashed_password)

# OAuth2 scheme untuk membaca token dari request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Secret key untuk JWT (harus sesuai dengan yang digunakan saat login)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  """Mendapatkan user yang sedang login berdasarkan token JWT."""
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication token",
    headers={"WWW-Authenticate": "Bearier"}
  )

  try:
    # Decode JWT
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email = str = payload.get("sub") # "sub" adalah subject (biasanya email user)
    if email is None:
      raise credentials_exception

    # Cari user berdasarkan email
    user = db.query(User).filter(User.email == email).first()
    if user is None:
      raise credentials_exception
    return user

  except PyJWTError:
    raise credentials_exception

def create_access_token(data: dict, expires_delta: timedelta):
  """Membuat JWT token dengan masa berlaku tertentu."""
  to_encode = data.copy()
  expire = datetime.utcnow() + expires_delta
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

