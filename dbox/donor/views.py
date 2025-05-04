from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from common.db_config import get_db
from .donor_serializer import DonorSerializer
from bson import ObjectId

# Create your views here.

class DonorListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        db = get_db()
        donors = list(db.donors.find())
        for donor in donors:
            donor["_id"] = str(donor["_id"])
            del donor["id"]
        return Response(donors, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            db = get_db()
            donor_data = serializer.validated_data
            
            if db.donors.find_one({"mobile_number": donor_data["mobile_number"]}):
                return Response({"error": "User with this mobile number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            employee_id = str(request.user.id)
            donor_data["employee_id"] = employee_id
            
            result = db.donors.insert_one(donor_data)
            
            response_data = donor_data.copy()
            response_data["_id"] = str(result.inserted_id)
            return Response({
                "message": "Donor created successfully",
                "data": response_data
                             }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DonorRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        db = get_db()
        donor = db.donors.find_one({"_id": pk})
        if donor:
            return Response(donor, status=status.HTTP_200_OK)
        return Response({"error": "Donor not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            db = get_db()
            donor_data = serializer.validated_data
            db.donors.update_one({"_id": pk}, {"$set": donor_data})
            return Response({"message": "Donor updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        db = get_db()
        result = db.donors.delete_one({"_id": pk})
        if result.deleted_count > 0:
            return Response({"message": "Donor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Donor not found"}, status=status.HTTP_404_NOT_FOUND)