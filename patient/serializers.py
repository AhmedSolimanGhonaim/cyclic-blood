from rest_framework import serializers
from .models import Patient



class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        extra_kwargs = {
            'blood_type': {'required': True},
            'status': {'required': False, 'default': 'normal'},
            'hospital': {'required': False, 'allow_null': True},
        }
        
    
    