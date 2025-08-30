import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database.database import db
import os
from dotenv import load_dotenv

load_dotenv()

SOURCE_1 = os.getenv("SOURCE_1")
SOURCE_1_URL = os.getenv("SOURCE_1_URL")
NEWS_COLLECTION = os.getenv("NEWS_COLLECTION")


def scrape_source1(limit: int = 20):
    url = SOURCE_1_URL
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    articles = []

    # Each story is inside <li> with class "story"
    for card in soup.select("li .story")[:limit]:
        try:
            # Title + link
            title_tag = card.select_one("h3.c-title a")
            title = title_tag.get_text(strip=True) if title_tag else None
            link = title_tag["href"] if title_tag else None

            # Image
            img_tag = card.select_one("img.c-lazy-image__img")
            image = img_tag["src"] if img_tag else None

            # Summary
            summary_tag = card.select_one("p.c-dek")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""

            # Author (optional)
            author_tag = card.select_one(".c-tagline a")
            author = author_tag.get_text(strip=True) if author_tag else "Unknown"

            if title and link:
                articles.append(
                    {
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "image": image,
                        "author": author,
                        "sourceName": SOURCE_1,
                        "timestamp": datetime.utcnow(),
                    }
                )
        except Exception as e:
            print(f"Error parsing card: {e}")

    return articles


## TODO: other scrapers to be built
def scrape_source2():
    pass


def scrape_source3():
    pass


def scrapers_runner(limit: int = 50):
    sources = [scrape_source1]  ## TODO: adding more scrapers
    new_articles = []
    for scraper in sources:
        articles = scraper()
        for article in articles:
            if len(new_articles) >= limit:
                return new_articles
            query = (
                db.collection(NEWS_COLLECTION)
                .where("title", "==", article["title"])
                .where("url", "==", article["url"])
                .stream()
            )
            exists = any(query)
            if not exists:
                db.collection(NEWS_COLLECTION).add(article)
                new_articles.append(article)
    return new_articles
