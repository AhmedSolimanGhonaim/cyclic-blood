from django.urls import path, include
from rest_framework.routers import DefaultRouter



from .views import HospitalViewSet, HospitalProfile


router = DefaultRouter()
router.register(r'', HospitalViewSet, basename='hospital')
urlpatterns = [
    path('me/', HospitalProfile.as_view(), name='hospital-profile'),
    # path('patients/', include('hospital.urls')),  # Include patient URLs under hospital
]
urlpatterns += router.urls