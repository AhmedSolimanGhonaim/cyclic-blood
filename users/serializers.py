from rest_framework import serializers


from .models import CustomUser
from donor.serializers import DonorSerializer
from hospital.serializers import HospitalSerializer
from donor.models import Donor
from hospital.models import Hospital
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'role', 'city']
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
        role = user_data.get('role')
        user = CustomUser.objects.create(user_data)
        if role == 'donor':
            Donor.objects.create(user=user, **validated_data['donor_profile'])
        elif role == 'hospital':
            Hospital.objects.create(
                user=user, **validated_data['hospital_profile'])

        return user
