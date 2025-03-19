from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.index import router as all_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan React lokal
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode (GET, POST, DELETE, dll.)
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(all_router)