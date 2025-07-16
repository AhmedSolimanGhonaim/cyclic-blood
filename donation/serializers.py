from datetime import timedelta
from rest_framework import serializers
from .models import Donation, DonationStatus


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
        # to block user from manipulating the virus test , logically set it to readonly
        read_only_fields = ['id', 'status',
                            'expiration_date', 'rejection_reason','virus_test_result']
        extra_kwargs = {
            'blood_type': {'required': True},
            
            'bank': {'required': True,},
        }
    def create(self, validated_data):
       
        return Donation.objects.create(**validated_data)
