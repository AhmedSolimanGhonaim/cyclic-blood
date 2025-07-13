from django.shortcuts import render

# Create your views here.
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        hospital = getattr(self.request.user, 'hospital_profile', None)
        if  hospital :
            serializer.save(hospital=hospital)
        else:
            return Response({"error": "You must be a hospital to create a patient."}, status=status.HTTP_403_FORBIDDEN)
    def get_queryset(self):
        if hasattr(self.request.user, 'hospital_profile'):
            return Patient.objects.filter(hospital=self.request.user.hospital_profile)
        return Patient.objects.none()
    