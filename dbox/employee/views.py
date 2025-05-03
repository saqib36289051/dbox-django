from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .db_config import get_db
from .auth_serializer import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

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
       data["role"] = "admin" if data["user_type"] == "admin" else "user"
       db.users.insert_one(data)
       return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
   

class LoginUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        db = get_db()
        user = db.users.find_one({"phone_number": data["phone_number"]})
        if user and check_password(data["password"], user["password"]):
            refresh = RefreshToken.for_user(type("user",(),{"id":str(user["_id"])}))
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_info": {
                    "id": str(user["_id"]),
                    "phone_number": user["phone_number"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                    "user_type": user["user_type"],
                },
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    