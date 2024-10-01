from django.urls import path
from .views import SignUpAPIView

urlpatterns = [
    path('user/', SignUpAPIView.as_view())
]