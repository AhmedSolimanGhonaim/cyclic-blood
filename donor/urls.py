from rest_framework.routers import DefaultRouter
from .views import DonorViewSet ,DonorProfile
from django.urls import path 


router = DefaultRouter()
router.register(r'', DonorViewSet, basename='donor')

urlpatterns = [
    path('me/', DonorProfile.as_view(), name='donor-profile'),
]
urlpatterns += router.urls
