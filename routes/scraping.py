from fastapi import APIRouter, WebSocket
from typing import List
from utils.scraper import scrapers_runner
from routes.websocket import broadcast_new_article

clients: List[WebSocket] = []

router = APIRouter()


@router.post("/scrape-now")
async def scrape_now():
    new_articles = scrapers_runner()
    for article in new_articles:
        await broadcast_new_article(article)
    return {
        "success": True,
        "new_articles_count": len(new_articles),
        "new_articles": new_articles,
    }
