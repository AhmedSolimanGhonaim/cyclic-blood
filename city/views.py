from rest_framework.viewsets import  ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .serializers import CitySerializer
from .models import City


@method_decorator(cache_page(60 * 60), name='list')  
@method_decorator(cache_page(60 * 60), name='retrieve')  
class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
