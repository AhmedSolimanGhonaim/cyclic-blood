# matchersystem/serializers.py

from rest_framework import serializers
from .models import Matcher
    

class MatcherSerializer(serializers.ModelSerializer):
    stock_info = serializers.SerializerMethodField()
    request_info = serializers.SerializerMethodField()

    class Meta:
        model = Matcher
        fields = ['id', 'quantity_allocated', 'stock_info', 'request_info']

    def get_stock_info(self, obj):
        return {
            "id": obj.stock_id.id,
            "blood_type": obj.stock_id.blood_type,
            "city": obj.stock_id.city,
            "status": obj.stock_id.status
        }

    def get_request_info(self, obj):
        request = obj.request_id
        return {
            "id": request.id,
            "blood_type": request.blood_type,
            "quantity": request.quantity,
            "priority": request.priority,
            "city": request.city,
            "hospital": request.hospital.name if request.hospital else None,
            "patient": request.patient.name if request.patient else None
        }
