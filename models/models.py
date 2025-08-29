from pydantic import BaseModel
from datetime import datetime


class NewsItem(BaseModel):
    title: str
    url: str
    summary: str
    image: str
    sourceName: str
    timestamp: datetime
