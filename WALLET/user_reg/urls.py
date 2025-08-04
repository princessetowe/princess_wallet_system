from django.urls import path
from .views import SignUpAPIView, WalletDetailView, WithdrawHistoryView

urlpatterns = [
    path('register/', SignUpAPIView.as_view()),
    path('wallet/', WalletDetailView.as_view()),
    path('withdrawals/history/', WithdrawHistoryView.as_view()),
]