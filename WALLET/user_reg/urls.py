from django.urls import path
from .views import SignUpAPIView, WalletDetailView, TransactionsView, WalletUpgradeView
urlpatterns = [
    path('register/', SignUpAPIView.as_view()),
    path('wallet/', WalletDetailView.as_view()),
    path('transactions/', TransactionsView.as_view()),
    path('upgrade/', WalletUpgradeView.as_view()),
]