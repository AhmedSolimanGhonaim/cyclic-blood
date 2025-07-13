from rest_framework import serializers
from .models import CustomUser
from donor.serializers import DonorSerializer
from hospital.serializers import HospitalSerializer
from donor.models import Donor
from hospital.models import Hospital


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id', 'username', 'password','email', 'role', 'city']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    
class RegistrationSerializer(serializers.Serializer):
    user = CustomUserSerializer()
    donor_profile = DonorSerializer(required=False)
    hospital_profile = HospitalSerializer(required=False)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        donor_data = validated_data.pop('donor_profile', None)
        hospital_data = validated_data.pop('hospital_profile', None)

        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        if user.role == 'donor' and donor_data:
            Donor.objects.create(user=user, **donor_data)
        elif user.role == 'hospital' and hospital_data:
            Hospital.objects.create(user=user, **hospital_data)

        return user
