from django.urls import path
from .views import MatcherListView

urlpatterns = [
    path('', MatcherListView.as_view(), name='matcher-list'),

]
