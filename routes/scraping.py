from fastapi import APIRouter, WebSocket, Query
from typing import Optional
from utils.scraper import scrapers_runner
from routes.websocket import broadcast_new_article

router = APIRouter(prefix="/scrape", tags=["Scraping"])


@router.post("")
async def scrape_now(
    limit: Optional[int] = Query(
        10, ge=1, le=100, description="Max number of articles to return"
    )
):
    new_articles = scrapers_runner(limit)
    limited_articles = new_articles[:limit]
    for article in limited_articles:
        await broadcast_new_article(article)

    return {
        "success": True,
        "new_articles_count": len(limited_articles),
        "new_articles": limited_articles,
    }
