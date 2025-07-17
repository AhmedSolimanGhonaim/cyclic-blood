from rest_framework import serializers
from .models import BloodBank
from .models import BankEmployee

class BankEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankEmployee
        fields = ['blood_bank']



class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model =BloodBank
        fields = '__all__'
        read_only_fields = ['id','created_at']
        