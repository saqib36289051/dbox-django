from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://msaqibdev:jp5AbYCMxJWqCAw6@cluster0.ljumcp1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
def get_db():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["dbox"]
    return db   