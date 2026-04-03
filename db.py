from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError(" MONGO_URI is missing")

try:
    client = MongoClient(MONGO_URI, tls=True)
    client.admin.command("ping")
    print(" MongoDB connected")
except Exception as e:
    print(" MongoDB error:", e)
    raise e

db = client["telegram_bot"]
collection = db["documents"]

def get_doc(keyword):
    return collection.find_one({"keyword": keyword})

def get_all_docs():
    return list(collection.find({}, {"_id": 0, "keyword": 1}))
