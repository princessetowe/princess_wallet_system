from django.urls import path
from .views import *

urlpatterns = [
    path('view/', WalletDetailView.as_view()),
    path('upgrade/', WalletUpgradeView.as_view()),
]