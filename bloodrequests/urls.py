from django.urls import path,include
from .views import BloodRequestCreateView , BloodRequestListView ,BatchMatchView

urlpatterns = [
    path('do/', BloodRequestCreateView.as_view(), name='blood-request-create'),
    path('', BloodRequestListView.as_view(), name='blood-request-list'),
    path('batch/',BatchMatchView.as_view(),name='batch')
]
