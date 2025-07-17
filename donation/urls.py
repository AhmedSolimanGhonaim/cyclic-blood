from django.urls import path, include


from .views import DonationCreationView , LabTestUpdate , DonationListViewInBank, DonorDonationHistoryView


urlpatterns = [
    path('create/', DonationCreationView.as_view(), name='donation-create'),
    path('test/<int:pk>/',LabTestUpdate.as_view(), name='lab-test' ),
    path('list/',DonationListViewInBank.as_view(), name='donation-list-in-bank' ),
    path('history/', DonorDonationHistoryView.as_view(), name='donation-history')
]