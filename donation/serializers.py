from datetime import timedelta
from rest_framework import serializers
from .models import Donation, DonationStatus


class DonationSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    donor_name = serializers.CharField(source='donor.name', read_only=True)

    class Meta:
        model = Donation
        fields = [
            'id', 'donor_name', 'donation_date', 'virus_test_result', 'blood_type',
            'quantity_ml', 'bank', 'bank_name', 'status', 'expiration_date', 'rejection_reason'
        ]
        read_only_fields = [
            'id', 'donor_name', 'donation_date', 'status', 'expiration_date',
            'rejection_reason', 'virus_test_result', 'bank_name'
        ]
        extra_kwargs = {
            'blood_type': {'required': True},
            'quantity_ml': {'required': True},
            'bank': {'required': True},
        }
    def create(self, validated_data):
       
        return Donation.objects.create(**validated_data)
