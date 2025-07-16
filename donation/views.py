from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Donation
from .serializers import DonationSerializer
from rest_framework.generics import UpdateAPIView
from bloodstock.models import Stock
from django.core.exceptions import ValidationError





class DonationCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, 'donor_profile'):
            return Response({"error": "Only donors can create donations."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            donation = serializer.save(donor=request.user.donor_profile)
            return Response(DonationSerializer(donation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabTestUpdate(UpdateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes= [IsAdminUser]

    
    def patch (self,request,*args, **kwargs):
        donation =self.get_object()
        donation.virus_test_result = True
        was_accepted= donation.evaluate_donation()
        donation.save()
        
        if was_accepted:
            # Only create stock if it doesn't already exist
            if not hasattr(donation, 'stock'):
                try:
                    Stock.objects.create(
                        donation=donation, blood_type=donation.blood_type)
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(DonationSerializer(donation).data)
