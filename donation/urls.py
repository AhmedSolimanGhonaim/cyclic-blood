from django.urls import path, include


from .views import DonationCreationView , LabTestUpdate


urlpatterns = [
    path('create/', DonationCreationView.as_view(), name='donation-create'),
    path('test/<int:pk>/',LabTestUpdate.as_view(), name='lab-test' )
]