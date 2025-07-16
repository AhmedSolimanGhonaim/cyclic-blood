from rest_framework import serializers
from .models import BloodBank



class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model =BloodBank
        fields = '__all__'
        read_only_fields = ['id','created_at']
        