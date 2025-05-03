
class MongoUser:
    def __init__(self, user_dict):
        self.id = str(user_dict["_id"])
        self.username = user_dict.get("phone_number", "")
        # Add other required attributes for JWT token
        self.is_active = True
        
    def __str__(self):
        return self.username