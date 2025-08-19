from django.urls import path
from .views import *

urlpatterns = [
    path('withdraw/', WithdrawCreateView.as_view()),
    path('deposit/', DepositCreateView.as_view()),
    path('transactions/', TransactionsView.as_view()),
]