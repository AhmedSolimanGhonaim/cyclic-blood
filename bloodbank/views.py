from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser , IsAuthenticatedOrReadOnly
from .models import BloodBank
from .serializers import BloodBankSerializer


class BloodBankViewSet(ModelViewSet):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]