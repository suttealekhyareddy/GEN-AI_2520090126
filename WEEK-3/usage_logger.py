import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017"
)

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)

db = client["genai_monitoring"]
collection = db["usage_logs"]


def log_usage(data):
    try:
        log_entry = {
            "timestamp": datetime.now(),
            "model": "llama3.2",
            "input_tokens": data.get("input_tokens", 0),
            "output_tokens": data.get("output_tokens", 0),
            "total_tokens": data.get("total_tokens", 0),
            "response_time": data.get("response_time", 0),
            "success": data.get("success", False),
            "response": data.get("response", "")
        }

        collection.insert_one(log_entry)
        print("Usage log saved to MongoDB successfully!")

    except Exception as error:
        print("MongoDB logging error:", error)