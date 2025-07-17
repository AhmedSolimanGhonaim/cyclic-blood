from django.urls import path 
from .views import UsersViewSett, UserRegistrationView, MyTokenObtainPairView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
router =DefaultRouter()
router.register(r'users', UsersViewSett, basename='users')
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls