from django.urls import path

from .views import StockSummary, StockCitySummary

urlpatterns = [
    path('summary/', StockSummary.as_view(), name='summary'),
    path('summary/city/', StockCitySummary.as_view(), name='stock-summary-city'),

]
