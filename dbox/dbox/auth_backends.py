from django.contrib.auth.backends import BaseBackend
from common.db_config import get_db
from bson import ObjectId
from .mongo_user import MongoUser

class MongoDBAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        db = get_db()
        phone_number = username
        
        user = db.users.find_one({"phone_number": phone_number})
        if user:
            return MongoUser(user)
            
        return None
        
    def get_user(self, user_id):
        try:
            db = get_db()
            user = db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                return MongoUser(user)
        except Exception:
            return None
        
        return None