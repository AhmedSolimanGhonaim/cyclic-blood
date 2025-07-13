from django.shortcuts import render
from .models import BloodRequests
from .serializers import BloodRequestSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class BloodRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def post(self,request):
        """CREATE A BLOOD REQUEST"""
        hospital = getattr(request.user,'hospital_profile', None)
        if not hospital : 
            return Response({"error": "You must be a hospital to create a blood request."}, status=status.HTTP_403_FORBIDDEN)
        serializer= BloodRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hospital=hospital)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BloodRequestListView(APIView):
    #  i added [is authenticated] here since i think we need to allow all users to see the blood requests
    permission_classes = [IsAuthenticated]
    def get(self,request):
        
        blood_requests = BloodRequests.objects.all()
        serializer = BloodRequestSerializer(blood_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    