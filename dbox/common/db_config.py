from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

uri = os.environ.get("MONGODB_URI")
print(f"MONGODB_URI: {uri}")
_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(uri, server_api=ServerApi('1'))
    db = _client["dbox"]
    return db