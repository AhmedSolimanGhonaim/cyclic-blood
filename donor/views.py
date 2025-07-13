
from rest_framework.viewsets import ModelViewSet 
from rest_framework.views import APIView
from .serializers import DonorSerializer
from .models import Donor


from django.shortcuts import get_object_or_404
# from   import get_user_model
from rest_framework.response import Response
class DonorProfile(APIView):
    def get(self,request):
        #  if self.request.user.is_authenticated:
             donor  = Donor.objects.filter(user=self.request.user)
             serializer = DonorSerializer(donor, many=True)
             return Response(serializer.data)

class DonorViewSet(ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
