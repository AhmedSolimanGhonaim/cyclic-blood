
from rest_framework.viewsets import ModelViewSet 
from rest_framework.views import APIView
from .serializers import DonorSerializer
from .models import Donor
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  ,IsAdminUser


from django.shortcuts import get_object_or_404
# from   import get_user_model
from rest_framework.response import Response
class DonorProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
            """
            Retrieve the donor profile for the authenticated user.
            """
            # Assuming you have a Donor model with a OneToOne relationship to User
            donor = get_object_or_404(Donor, user=request.user)
            serializer = DonorSerializer(donor)
            return Response(serializer.data)

class DonorViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    
    
