from django.urls import path
from .views import  WithdrawCreateView

urlpatterns = [
    path('withdraw/', WithdrawCreateView.as_view())
]