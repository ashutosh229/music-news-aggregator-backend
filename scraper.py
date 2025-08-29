import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.database import db
from app.routes.websocket import broadcast_new_article
