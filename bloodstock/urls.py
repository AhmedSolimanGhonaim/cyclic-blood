from django.urls import path 

from .views import StockSummary

urlpatterns = [
    path('summary/',StockSummary.as_view(),name='summary')
    
]
