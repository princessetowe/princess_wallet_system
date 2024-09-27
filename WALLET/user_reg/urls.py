from django.urls import path
from .views import SignupAPIView

urlpatterns = [
    path('user/', SignupAPIView.as_view())
]