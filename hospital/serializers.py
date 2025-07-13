from rest_framework import serializers
from .models import Hospital



class HospitalSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    city = serializers.CharField(source='user.city', read_only=True)
    class Meta:
        model = Hospital
        exclude = ['user']