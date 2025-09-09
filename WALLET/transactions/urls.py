from django.urls import path
from .views import *
from .webhookview import PaystackWebhookView
urlpatterns = [
    path('withdraw/', WithdrawCreateView.as_view()),
    path('deposit/', DepositCreateView.as_view()),
    path('list/', TransactionsView.as_view()),
    path("paystack/webhook/", PaystackWebhookView.as_view(), name="paystack_webhook"),
]