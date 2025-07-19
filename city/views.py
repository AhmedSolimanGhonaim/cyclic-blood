from rest_framework.viewsets import  ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .serializers import CitySerializer
from .models import City


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
