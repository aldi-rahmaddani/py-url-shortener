from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import url_shortener

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan React lokal
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode (GET, POST, DELETE, dll.)
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(url_shortener.router)