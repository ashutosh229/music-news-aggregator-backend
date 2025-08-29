from fastapi import FastAPI
from dotenv import load_dotenv
from routes import scraping
from routes import websocket
from routes import news
from routes import admin

load_dotenv()

app = FastAPI()

app.include_router(scraping.router)
app.include_router(websocket.router)
app.include_router(news.router)
app.include_router(admin.router)
