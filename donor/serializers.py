from rest_framework import serializers


from .models import Donor


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Donor
        exclude = ['user']
  