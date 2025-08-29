from fastapi import FastAPI
from dotenv import load_dotenv
from routes import scraping
from utils.scraper import scrapers_runner
import asyncio

load_dotenv()

app = FastAPI()

app.include_router(scraping.router)


@app.on_event("startup")
async def start_scraping():
    async def scraper_loop():
        while True:
            scrapers_runner()
            await asyncio.sleep(300)

    asyncio.create_task(scraper_loop())
