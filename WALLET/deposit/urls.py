from django.urls import path
from .views import DepositCreateView

urlpatterns = [
    path('deposit/', DepositCreateView.as_view()),
]