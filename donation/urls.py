from django.urls import path, include


from .views import DonationCreationView , LabTestUpdate , DonationListViewInBank, DonorDonationHistoryView, LabTestAcceptView, LabTestRejectView


urlpatterns = [
    path('create/', DonationCreationView.as_view(), name='donation-create'),
    path('test/<int:pk>/',LabTestUpdate.as_view(), name='lab-test' ),
    path('accept/<int:donation_id>/', LabTestAcceptView.as_view(), name='donation-accept'),
    path('reject/<int:donation_id>/', LabTestRejectView.as_view(), name='donation-reject'),
    path('list/',DonationListViewInBank.as_view(), name='donation-list-in-bank' ),
    path('history/', DonorDonationHistoryView.as_view(), name='donation-history')
]