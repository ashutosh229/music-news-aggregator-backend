from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from routes import scraping
from routes import websocket
from routes import news
from routes import admin

load_dotenv()

app = FastAPI()

origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## http://localhost:8080/static/admin.html
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(scraping.router)
app.include_router(websocket.router)
app.include_router(news.router)
app.include_router(admin.router)
