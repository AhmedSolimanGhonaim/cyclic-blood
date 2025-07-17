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
        fields = ['id', 'patient', 'quantity', 'city', 'status', 'priority', 'blood_type', 'requested_at', 'updated_at']
        read_only_fields = ['id', 'requested_at', 'updated_at', 'blood_type', 'priority', 'status']

    def create(self, validated_data):
        patient = validated_data.pop('patient', None)
        if not patient:
           raise serializers.ValidationError(
                "Patient is required to infer blood type and priority.")

        if patient:
            validated_data['blood_type'] = patient.blood_type
            validated_data['priority'] = patient.status
            validated_data['patient'] = patient
        return super().create(validated_data)
