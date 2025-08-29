from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")


def verify_admin(auth: str = Header(None)):
    if auth != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
