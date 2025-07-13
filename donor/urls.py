from rest_framework.routers import DefaultRouter
from .views import DonorViewSet ,DonorProfile
from django.urls import path , include
router = DefaultRouter()
router.register(r'donors', DonorViewSet, basename='donor')
urlpatterns = [
    path('/donor/', include(router.urls)),
    path('/donor/profile/', DonorProfile.as_view(), name='donor-profile'),
]
urlpatterns += router.urls
