from fastapi import FastAPI
from routers import url_shortener

app = FastAPI()
app.include_router(url_shortener.router)