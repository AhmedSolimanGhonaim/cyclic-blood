from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from .models import Donation
from .serializers import DonationSerializer
from rest_framework.generics import UpdateAPIView
from bloodstock.models import Stock
from django.core.exceptions import ValidationError
from bloodbank.bank_permission import IsBankEmployee

from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist


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

class DonationListViewInBank(ListAPIView):
    permission_classes = [IsBankEmployee]
    serializer_class = DonationSerializer
    def get_queryset(self):
        bank = self.request.user.bank_employee_profile.blood_bank
        return Donation.objects.filter(bank=bank)

      
class LabTestUpdate(UpdateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    # permission_classes= [IsAdminUser]
    permission_classes = [IsBankEmployee]
    def patch (self,request,*args, **kwargs):
        if not hasattr(request.user, 'bank_employee_profile'):
            return Response({"error": "Only bank employees can update donations."}, status=status.HTTP_403_FORBIDDEN)
        if not request.user.bank_employee_profile.blood_bank:
            return Response({"error": "Bank employee must be associated with a bank."}, status=status.HTTP_403_FORBIDDEN)
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


class DonorDonationHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DonationSerializer

    def get_queryset(self):
        try:
            # Check if the user has a donor profile and return their donations
            donor_profile = self.request.user.donor_profile
            return Donation.objects.filter(donor=donor_profile).order_by('-created_at')
        except ObjectDoesNotExist:
            # If the user is not a donor (e.g., hospital, admin), return an empty queryset
            return Donation.objects.none()
