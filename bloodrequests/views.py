from django.shortcuts import render
from .models import BloodRequests
from .serializers import BloodRequestSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsHospitalUser

from matchersystem.services import match_blood_request ,batch_match_requests




class BloodRequestCreateView(APIView):
    permission_classes = [IsHospitalUser]
    
    def post(self,request):
        """CREATE A BLOOD REQUEST"""
        serializer= BloodRequestSerializer(data=request.data)
        if serializer.is_valid():
            blood_request = serializer.save(hospital=request.user.hospital_profile)
            match_blood_request(blood_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        

class BloodRequestListView(APIView):
    permission_classes = [IsHospitalUser]
    def get(self,request):
        blood_requests = BloodRequests.objects.filter(hospital=request.user.hospital_profile).order_by('-requested_at')
        serializer = BloodRequestSerializer(blood_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class BatchMatchView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        result = batch_match_requests()
        return Response(result)
