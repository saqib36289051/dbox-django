from rest_framework_simplejwt.authentication import JWTAuthentication
from common.db_config import get_db
from bson import ObjectId
from .mongo_user import MongoUser

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            db = get_db()
            user_data = db.users.find_one({"_id": ObjectId(user_id)})
            
            if user_data:
                return MongoUser(user_data)
            return None
        except Exception as e:
            return None