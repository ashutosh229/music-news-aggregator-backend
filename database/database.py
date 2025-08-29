import firebase_admin
from firebase_admin import credentials, firestore
import os

CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH")

cred = credentials.Certificate(CERTIFICATE_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
