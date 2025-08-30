import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database.database import db
import os
from dotenv import load_dotenv

load_dotenv()

SOURCE_1 = os.getenv("SOURCE_1")
SOURCE_1_URL = os.getenv("SOURCE_1_URL")
SOURCE_2 = os.getenv("SOURCE_2")
SOURCE_2_URL = os.getenv("SOURCE_2_URL")
SOURCE_3 = os.getenv("SOURCE_3")
SOURCE_3_URL = os.getenv("SOURCE_3_URL")
NEWS_COLLECTION = os.getenv("NEWS_COLLECTION")


def scrape_source1():
    url = SOURCE_1_URL
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    articles = []
    for card in soup.select("li .story"):
        try:
            title_tag = card.select_one("h3.c-title a")
            title = title_tag.get_text(strip=True) if title_tag else None
            link = title_tag["href"] if title_tag else None
            img_tag = card.select_one("img.c-lazy-image__img")
            image = img_tag["src"] if img_tag else None
            summary_tag = card.select_one("p.c-dek")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
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


def scrape_source2():
    url = SOURCE_2_URL
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    articles = []
    for card in soup.select("div.tdb_module_loop"):
        try:
            title_tag = card.select_one("h3.entry-title a")
            title = title_tag.get_text(strip=True) if title_tag else None
            link = title_tag["href"] if title_tag else None
            img_tag = card.select_one("span.entry-thumb")
            image = (
                img_tag["data-img-retina-url"]
                if img_tag and img_tag.has_attr("data-img-retina-url")
                else (
                    img_tag["data-img-url"]
                    if img_tag and img_tag.has_attr("data-img-url")
                    else None
                )
            )
            summary_tag = card.select_one("div.td-excerpt")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            author = "NME Staff"
            if title and link:
                articles.append(
                    {
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "image": image,
                        "author": author,
                        "sourceName": SOURCE_2,
                        "timestamp": datetime.utcnow(),
                    }
                )
        except Exception as e:
            print(f"Error parsing NME card: {e}")
    return articles


def scrape_source3():
    url = SOURCE_3_URL
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    articles = []
    for card in soup.select("div.SummaryItemWrapper-ircKXK"):
        try:
            title_tag = card.select_one("h3.SummaryItemHedBase-hnYOxl")
            link_tag = card.select_one("a.SummaryItemHedLink-cxRzVg")
            title = title_tag.get_text(strip=True) if title_tag else None
            link = (
                "https://pitchfork.com" + link_tag["href"]
                if link_tag and link_tag.has_attr("href")
                else None
            )
            img_tag = card.select_one("img.responsive-image__image")
            image = img_tag["src"] if img_tag and img_tag.has_attr("src") else None
            author_tag = card.select_one("span.BylineName-kqTBDS")
            author = (
                author_tag.get_text(strip=True).replace("By ", "")
                if author_tag
                else "Unknown"
            )
            date_tag = card.select_one("time.summary-item__publish-date")
            if date_tag:
                try:
                    published_date = datetime.strptime(
                        date_tag.get_text(strip=True), "%B %d, %Y"
                    )
                except ValueError:
                    published_date = datetime.utcnow()
            else:
                published_date = datetime.utcnow()
            summary = ""
            if title and link:
                articles.append(
                    {
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "image": image,
                        "author": author,
                        "sourceName": SOURCE_3_URL,
                        "timestamp": published_date,
                    }
                )
        except Exception as e:
            print(f"Error parsing Pitchfork card: {e}")
    return articles


def scrapers_runner(limit):
    sources = [scrape_source1, scrape_source2, scrape_source3]
    new_articles = []
    for scraper in sources:
        articles = scraper()
        for article in articles:
            if len(new_articles) >= limit:
                return new_articles
            query = (
                db.collection("news")
                .where("title", "==", article["title"])
                .where("url", "==", article["url"])
                .stream()
            )
            exists = any(query)
            if not exists:
                db.collection(NEWS_COLLECTION).add(article)
                new_articles.append(article)
    return new_articles
