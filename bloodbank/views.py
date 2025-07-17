from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from bloodstock.models import Stock
from bloodstock.serializers import StockSerializer
from rest_framework.permissions import IsAdminUser , IsAuthenticatedOrReadOnly
from .models import BloodBank
from .serializers import BloodBankSerializer


class BloodBankViewSet(ModelViewSet):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ['list','retrieve', 'stock']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]

    @action(detail=True, methods=['get'])
    def stock(self, request, pk=None):
        bank = self.get_object()
        stocks = Stock.objects.filter(bank=bank)
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)