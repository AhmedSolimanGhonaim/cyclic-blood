from rest_framework import serializers 
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model  """
    class Meta :
        model = Stock
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    # def create(self, validated_data):
    #     return super().create(validated_data)