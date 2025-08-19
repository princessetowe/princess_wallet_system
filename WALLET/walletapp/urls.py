from django.urls import path
from .views import *

urlpatterns = [
    path('wallet/', WalletDetailView.as_view()),
    path('upgrade/', WalletUpgradeView.as_view()),
]