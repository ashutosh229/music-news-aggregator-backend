from fastapi import APIRouter, Header, HTTPException
from database.database import db
from models.models import NewsItem
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import os
from utils.admin import verify_admin

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")


router = APIRouter(prefix="/admin", tags=["Admin"])


## http://127.0.0.1:8080/admin/news
@router.post("/news")
def add_news(news: NewsItem, authorization: str = Header(None)):
    verify_admin(authorization)
    doc_ref = db.collection("news").add(news.dict())
    return {"success": True, "message": "News added successfully", "id": doc_ref[1].id}


## http://127.0.0.1:8080/admin/news/1
@router.put("/news/{news_id}")
def edit_news(news_id: str, news: dict, authorization: str = Header(None)):
    verify_admin(authorization)
    db.collection("news").document(news_id).update(news)
    return {"success": True, "message": "News updated successfully"}


## http://127.0.0.1:8080/admin/news/1
@router.delete("/news/{news_id}")
def delete_news(news_id: str, authorization: str = Header(None)):
    verify_admin(authorization)
    db.collection("news").document(news_id).delete()
    return {"success": True, "message": "News deleted successfully"}


## http://127.0.0.1:8080/admin/news
@router.get("/news")
def get_all_news(
    source: Optional[str] = None,
    date: Optional[str] = None,
    authorization: str = Header(None),
):
    verify_admin(authorization)
    query = db.collection("news")

    if source:
        query = query.where("sourceName", "==", source)

    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            next_day = date_obj.replace(hour=23, minute=59, second=59)
            query = query.where("timestamp", ">=", date_obj).where(
                "timestamp", "<=", next_day
            )
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
            )

    docs = query.stream()
    return {"success": True, "data": [{**doc.to_dict(), "id": doc.id} for doc in docs]}
