from fastapi import FastAPI
from dotenv import load_dotenv
from routes import scraping
from routes import websocket
from routes import news

load_dotenv()

app = FastAPI()

app.include_router(scraping.router)
app.include_router(websocket.router)
app.include_router(app.router)
