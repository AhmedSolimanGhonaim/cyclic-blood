from rest_framework import serializers 
from .models import BloodStock

class BloodStockSerializer(serializers.ModelSerializer):
    """Serializer for BloodStock model  """
    class Meta :
        model = BloodStock
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    # def create(self, validated_data):
    #     return super().create(validated_data)