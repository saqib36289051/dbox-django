from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.environ.get("MONGODB_URI")
_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(uri, server_api=ServerApi('1'))
    db = _client["dbox"]
    return db