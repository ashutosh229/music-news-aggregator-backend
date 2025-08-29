import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import db
import os

SOURCE_1 = os.getenv("SOURCE_1")
NEWS_COLLECTION = os.getenv("NEWS_COLLECTION")


def scrape_source1():
    url = "https://www.rollingstone.com/music/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    articles = []
    for card in soup.select(".c-card"):
        title = card.get_text(strip=True)
        link = card.find("a")["href"] if card.find("a") else None
        image = card.find("img")["src"] if card.find("img") else None
        summary = card.find("p").get_text(strip=True) if card.find("p") else ""
        if title and link:
            articles.append(
                {
                    "title": title,
                    "url": link,
                    "summary": summary,
                    "image": image,
                    "sourceName": SOURCE_1,
                    "timestamp": datetime.utcnow(),
                }
            )
    return articles


## TODO: other scrapers to be built
def scrape_source2():
    pass


def scrape_source3():
    pass


def scrapers_runner():
    sources = [scrape_source1, scrape_source2, scrape_source3]
    for scraper in sources:
        articles = scraper()
        for article in articles:
            query = (
                db.collection(NEWS_COLLECTION)
                .where("title", "==", article["title"])
                .where("url", "==", article["url"])
                .stream()
            )
            exists = any(query)
            if not exists:
                doc_ref = db.collection(NEWS_COLLECTION).add(article)
                ## TODO: add the broadcasting mechanism
