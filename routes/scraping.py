from fastapi import APIRouter, WebSocket, Query
from typing import Optional
from utils.scraper import scrapers_runner
from routes.websocket import broadcast_new_article

router = APIRouter(prefix="/scrape", tags=["Scraping"])


## http://localhost:8080/scrape?limit=10
@router.post("")
async def scrape_now(
    limit: Optional[int] = Query(
        10, ge=1, le=100, description="Max number of articles to return"
    )
):
    new_articles = scrapers_runner(limit)
    for article in new_articles:
        await broadcast_new_article(article)

    return {
        "success": True,
        "new_articles_count": len(new_articles),
        "new_articles": new_articles,
    }
