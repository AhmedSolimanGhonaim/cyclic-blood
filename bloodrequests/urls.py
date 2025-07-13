from django.urls import path,include
from .views import BloodRequestCreateView , BloodRequestListView

urlpatterns = [
    path('do/', BloodRequestCreateView.as_view(), name='blood-request-create'),
    path('', BloodRequestListView.as_view(), name='blood-request-list'),
]
