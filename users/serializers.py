from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from donor.serializers import DonorSerializer
from hospital.serializers import HospitalSerializer
from donor.models import Donor
from hospital.models import Hospital
import re
from bloodbank.serializers import BankEmployeeSerializer
from bloodbank.models import BankEmployee
from city.models import City
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id', 'username', 'password','email', 'role', 'city']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate_password(self,value):
        # Must be 8+ chars, include upper/lowercase and number
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@#$%^&+=]{8,}$', value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long, contain one uppercase letter and one number."
            )
        return value

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
    bank_employee_profile = BankEmployeeSerializer(required=False)
    
    def validate(self, data):
        if 'user' in data and 'city' in data['user']:
            city_value = data['user']['city']
            if hasattr(city_value, 'id'):
                data['user']['city'] = city_value.id
        return data
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        donor_data = validated_data.pop('donor_profile', None)
        hospital_data = validated_data.pop('hospital_profile', None)
        bank_employee_data = validated_data.pop('bank_employee_profile', None)

        password = user_data.pop('password')
        city_id = user_data.pop('city', None)
        
        user = CustomUser(**user_data)
        if city_id:
            user.city = City.objects.get(id=city_id)
        user.set_password(password)
        user.save()

        if user.role == 'donor' and donor_data:
            Donor.objects.create(user=user, **donor_data)
        elif user.role == 'hospital' and hospital_data:
            Hospital.objects.create(user=user, **hospital_data)
        elif user.role == 'bank_employee' and bank_employee_data:
            BankEmployee.objects.create(user=user, **bank_employee_data)
        return user

class UserLoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'city']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserLoginResponseSerializer(self.user)
        data['user'] = serializer.data
        return data
