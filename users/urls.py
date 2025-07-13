from django.urls import path 
from .views import UsersViewSett, UserRegistrationView
from rest_framework.routers import DefaultRouter
router =DefaultRouter()
router.register(r'users', UsersViewSett, basename='users')
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]
