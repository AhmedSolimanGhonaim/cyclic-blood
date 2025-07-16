from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .models import Stock
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class StockSummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = Stock.count_available_blood()
        return Response(summary)


class StockCitySummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = Stock.count_available_blood_by_city()
        return Response(summary)
