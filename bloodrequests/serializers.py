from rest_framework import serializers
from .models import BloodRequests
from patient.models import Patient


class BloodRequestSerializer(serializers.ModelSerializer):
    """
    Secure patient data:
    - `patient`: write-only → accepted in request, hidden in response
    - `blood_type` and `priority`: auto-set from the patient
    """
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        required=False,
        write_only=True
    )

    blood_type = serializers.CharField(read_only=True)  

    class Meta:
        model = BloodRequests
        exclude = ['hospital']  # we set this from the view
        read_only_fields = ['id', 'requested_at', 'updated_at']

    def create(self, validated_data):
        patient = validated_data.pop('patient', None)
        if patient:
            validated_data['blood_type'] = patient.blood_type
            validated_data['priority'] = patient.status
            validated_data['patient'] = patient
        return super().create(validated_data)
