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
from users.permissions import IsDonorUser

from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist


class DonationCreationView(APIView):
    permission_classes = [IsDonorUser]

    def post(self, request):
        donor = request.user.donor_profile
        blood_type = request.data.get('blood_type')
        
        # Check 90-day donation interval restriction
        days_until_next = donor.days_until_next_donation
        if days_until_next > 0:
            return Response(
                {
                    'error': f'You must wait {days_until_next} more days before your next donation. Last donation was on {donor.last_donation_date}.',
                    'days_remaining': days_until_next,
                    'last_donation_date': donor.last_donation_date
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if donor already has a blood type set
        if donor.blood_type and donor.blood_type != blood_type:
            return Response(
                {'error': f'Blood type cannot be changed. Your registered blood type is {donor.blood_type}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate blood bank selection
        bank_id = request.data.get('bank')
        if not bank_id:
            return Response(
                {'error': 'Blood bank selection is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            donation = serializer.save(donor=donor)
            
            # Set donor's blood type if this is their first donation
            if not donor.blood_type:
                donor.blood_type = blood_type
                donor.save(update_fields=['blood_type'])
            
            # Update donor's total donations and last donation date
            donor.total_donations += 1
            donor.last_donation_date = donation.donation_date
            donor.save(update_fields=['total_donations', 'last_donation_date'])
            
            return Response(DonationSerializer(donation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonationListViewInBank(ListAPIView):
    permission_classes = [IsBankEmployee]
    serializer_class = DonationSerializer
    def get_queryset(self):
        bank = self.request.user.bank_employee_profile.blood_bank
        return Donation.objects.filter(bank=bank)

      
class LabTestAcceptView(APIView):
    """Accept a donation after lab test"""
    permission_classes = [IsBankEmployee]
    
    def post(self, request, donation_id):
        try:
            donation = Donation.objects.get(id=donation_id)
            
            # Verify bank employee can manage this donation
            if donation.bank != request.user.bank_employee_profile.blood_bank:
                return Response(
                    {'error': 'You can only manage donations for your blood bank'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if donation is in pending status
            if donation.status != 'pending':
                return Response(
                    {'error': f'Cannot accept donation with status: {donation.status}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Accept the donation
            donation.virus_test_result = True
            donation.status = 'accepted'
            donation.save()
            
            # Create stock entry
            if not hasattr(donation, 'stock'):
                try:
                    Stock.objects.create(
                        donation=donation, 
                        blood_type=donation.blood_type,
                        blood_bank=donation.bank,
                        quantity=donation.quantity_ml
                    )
                    
                    # Send acceptance notification
                    from notification.services import NotificationService
                    NotificationService.notify_donation_accepted(donation)
                    
                except ValidationError as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'message': 'Donation accepted successfully',
                'donation': DonationSerializer(donation).data
            }, status=status.HTTP_200_OK)
            
        except Donation.DoesNotExist:
            return Response({'error': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)

class LabTestRejectView(APIView):
    """Reject a donation after lab test"""
    permission_classes = [IsBankEmployee]
    
    def post(self, request, donation_id):
        try:
            donation = Donation.objects.get(id=donation_id)
            
            # Verify bank employee can manage this donation
            if donation.bank != request.user.bank_employee_profile.blood_bank:
                return Response(
                    {'error': 'You can only manage donations for your blood bank'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if donation is in pending status
            if donation.status != 'pending':
                return Response(
                    {'error': f'Cannot reject donation with status: {donation.status}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get rejection reason
            reason = request.data.get('reason', 'Failed lab test requirements')
            
            # Reject the donation
            donation.virus_test_result = False
            donation.status = 'rejected'
            donation.save()
            
            # Send rejection notification
            from notification.services import NotificationService
            NotificationService.notify_donation_rejected(donation, reason)
            
            return Response({
                'message': 'Donation rejected successfully',
                'donation': DonationSerializer(donation).data
            }, status=status.HTTP_200_OK)
            
        except Donation.DoesNotExist:
            return Response({'error': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)

class LabTestUpdate(UpdateAPIView):
    """Legacy endpoint - kept for backward compatibility"""
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsBankEmployee]
    
    def patch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'bank_employee_profile'):
            return Response({"error": "Only bank employees can update donations."}, status=status.HTTP_403_FORBIDDEN)
        if not request.user.bank_employee_profile.blood_bank:
            return Response({"error": "Bank employee must be associated with a bank."}, status=status.HTTP_403_FORBIDDEN)
        
        donation = self.get_object()
        
        # Verify bank employee can manage this donation
        if donation.bank != request.user.bank_employee_profile.blood_bank:
            return Response(
                {'error': 'You can only manage donations for your blood bank'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        donation.virus_test_result = True
        was_accepted = donation.evaluate_donation()
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
            return Donation.objects.filter(donor=donor_profile).order_by('-donation_date')
        except ObjectDoesNotExist:
            # If the user is not a donor (e.g., hospital, admin), return an empty queryset
            return Donation.objects.none()
