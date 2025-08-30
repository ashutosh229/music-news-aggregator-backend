import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH")
print(CERTIFICATE_PATH)

cred = credentials.Certificate(CERTIFICATE_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client(database_id="music-db")
