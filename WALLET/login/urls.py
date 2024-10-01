from django.urls import path
from .views import LoginAPIView

urlpatterns = [
    path('user/', LoginAPIView.as_view())
]