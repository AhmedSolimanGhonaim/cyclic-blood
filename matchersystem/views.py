# matchersystem/views.py

from rest_framework.generics import ListAPIView
from .models import Matcher
from .serializers import MatcherSerializer
from rest_framework.permissions import  IsAuthenticated


class MatcherListView(ListAPIView):
    queryset = Matcher.objects.all().select_related(
        'stock_id', 'request_id__hospital', 'request_id__patient')
    serializer_class = MatcherSerializer
    permission_classes = [IsAuthenticated]


