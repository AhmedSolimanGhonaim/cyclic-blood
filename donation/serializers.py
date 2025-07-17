from datetime import timedelta
from rest_framework import serializers
from .models import Donation, DonationStatus


class DonationSerializer(serializers.ModelSerializer):
    bank = serializers.StringRelatedField(read_only=True)
    donor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Donation
        fields = [
            'id', 'donor', 'donation_date', 'virus_test_result', 'blood_type',
            'quantity_ml', 'bank', 'status', 'expiration_date', 'rejection_reason'
        ]
        read_only_fields = [
            'id', 'donor', 'donation_date', 'status', 'expiration_date',
            'rejection_reason', 'virus_test_result', 'bank'
        ]
        extra_kwargs = {
            'blood_type': {'required': True},
            'quantity_ml': {'required': True},
        }
    def create(self, validated_data):
       
        return Donation.objects.create(**validated_data)
