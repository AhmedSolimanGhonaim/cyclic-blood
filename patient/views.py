# from django.shortcuts import render

# # Create your views here.
# from .models import Patient
# from .serializers import PatientSerializer
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
# from rest_framework import status

# class PatientViewSet(ModelViewSet):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     def perform_create(self, serializer):
#         hospital = getattr(self.request.user, 'hospital_profile', None)
#         if  hospital :
#             serializer.save(hospital=hospital)
#         else:
#             return Response({"error": "You must be a hospital to create a patient."}, status=status.HTTP_403_FORBIDDEN)
#     def get_queryset(self):
#         if hasattr(self.request.user, 'hospital_profile'):
#             return Patient.objects.filter(hospital=self.request.user.hospital_profile)
#         return Patient.objects.none()
    
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        hospital = getattr(request.user, 'hospital_profile', None)
        if not hospital:
            return Response({"error": "You must be a hospital to create a patient."},status=status.HTTP_403_FORBIDDEN )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(hospital=hospital)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if hasattr(self.request.user, 'hospital_profile'):
            return Patient.objects.filter(hospital=self.request.user.hospital_profile)
        return Patient.objects.none()
