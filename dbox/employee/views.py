from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from common.db_config import get_db
from .auth_serializer import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from dbox.mongo_user import MongoUser

# Create your views here.
class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        db = get_db()
        
        if db.users.find_one({"phone_number": data["phone_number"]}):
            return Response({"error": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        data["password"] = make_password(data["password"])
        
        result = db.users.insert_one(data)
        
        # Return the user ID in the response
        return Response({
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }, status=status.HTTP_201_CREATED)

class LoginUser(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        data = request.data
        db = get_db()
        
        user = db.users.find_one({"phone_number": data["phone_number"]})
        
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)
            
        if user and check_password(data["password"], user["password"]):
            # Create a proper user object for JWT
            mongo_user = MongoUser(user)
            
            # Generate token with the custom user object
            refresh = RefreshToken.for_user(mongo_user)
            
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_info": {
                    "id": str(user["_id"]),
                    "phone_number": user["phone_number"],
                    "first_name": user.get("first_name", ""),
                    "last_name": user.get("last_name", ""),
                    "email": user.get("email", ""),
                    "user_type": user.get("user_type", ""),
                },
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)