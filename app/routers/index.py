from fastapi import APIRouter
from app.routers.auth import router as auth_router
from app.routers.url import router as url_router

router = APIRouter()

@router.get("/")
def root():
  return {"message": "Welcome to the URL Shortener API"}

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(url_router, prefix="/short", tags=["URL Shortener"])