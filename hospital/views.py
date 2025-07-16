from .models import Hospital

from .serializers import HospitalSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response





class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]
   

class HospitalProfile(APIView):
    permission_classes = [IsAuthenticated]    
    def get(self, request):
        if  request.user.role == 'hospital':
            """
            Retrieve the hospital profile for the authenticated user.
            """
            # Assuming you have a Hospital model with a OneToOne relationship to User
            hospital = get_object_or_404(Hospital, user=request.user)
        serializer = HospitalSerializer(hospital)
        return Response(serializer.data)
