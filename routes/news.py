from fastapi import APIRouter, HTTPException, Query
from database.database import db
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

NEWS_COLLECTION = os.getenv("NEWS_COLLECTION")

router = APIRouter(prefix="/news", tags=["Public News APIs"])


## http://127.0.0.1:8080/news
@router.get("")
def get_all_news():
    try:
        docs = db.collection(NEWS_COLLECTION).order_by("timestamp").stream()
        news = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return {"success": True, "message": "News fetched successfully", "data": news}
    except Exception as e:
        return {"success": False, "message": str(e)}


## http://127.0.0.1:8080/news/latest
@router.get("/latest")
def get_latest_news():
    try:
        one_hour_ago = datetime.utcnow() - timedelta(minutes=60)
        docs = (
            db.collection(NEWS_COLLECTION)
            .where("timestamp", ">=", one_hour_ago)
            .stream()
        )
        news = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return {
            "success": True,
            "message": "Latest news fetched successfully",
            "data": news,
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


## http://127.0.0.1:8080/news/search?query=Tyler
@router.get("/search")
def search_news(
    query: str = Query(None, description="Keyword to search in news titles/summary")
):
    try:
        if not query:
            return {"success": True, "message": "No query provided"}
        docs = db.collection("news").stream()
        results = []
        for doc in docs:
            item = doc.to_dict()
            if (
                query.lower() in item.get("title", "").lower()
                or query.lower() in item.get("summary", "").lower()
            ):
                results.append({**item, "id": doc.id})

        return {
            "success": True,
            "message": "News fetched successfully",
            "data": results,
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
