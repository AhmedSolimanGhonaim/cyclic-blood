from rest_framework import serializers
from .models import BloodBank
from .models import BankEmployee


# from .models import City
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class BankEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankEmployee
        fields = ['blood_bank']



class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model =BloodBank
        fields = '__all__'
        read_only_fields = ['id','created_at']

class BloodBankGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BloodBank
        geo_field = "location"  
        fields = ("id", "name", "city", "email", "phone")
