import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

print("DEBUG MONGO_URI:", MONGO_URI)

try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    print("✅ MongoDB connected")
except Exception as e:
    print("❌ MongoDB error:", e)
    raise e
