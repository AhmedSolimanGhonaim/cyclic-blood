from rest_framework import serializers
from .models import BloodRequests


class BloodRequestSerializer(serializers.ModelSerializer):
  
        """   to secure patient data, I will not include patient in the serializer
       but I will allow it to be set when creating a request
       this way, I can still link the request to a patient without exposing patient data
          """
        patient = serializers.PrimaryKeyRelatedField( queryset=BloodRequests._meta.get_field('patient').related_model.objects.all(), required=False, write_only=True )

        class Meta:
            model = BloodRequests
            exclude = ['hospital']
            read_only_fields = ['id', 'requested_at', 'updated_at']
            extra_kwargs = {
                'status': {'required': False, 'default': 'pending'},
                'priority': {'required': False, 'default': 'normal'},
            }

        def create(self, validated_data):
            patient = validated_data.get('patient')
            if patient:
                validated_data['blood_type'] = patient.blood_type
                validated_data['priority'] = patient.status
            return super().create(validated_data)