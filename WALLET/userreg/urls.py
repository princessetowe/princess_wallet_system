from django.urls import path
from .views import *

urlpatterns = [
    path('register/', SignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('kyc/upload/', KYCUploadView.as_view(), name='kyc-upload'),
    path('kyc/verify/<int:pk>/', KYCVerifyView.as_view(), name='kyc-verify'),
    path('wallet/upgrade/', WalletUpgradeAPIView.as_view(), name='wallet-upgrade'),
    path('adminprofile/', AdminProfileView.as_view(), name='admin-profile'),
    path('createadmin/', AdminProfileCreateView.as_view(), name="admin-profile-create"),
    path('verify-email/<str:token>/', VerifyEmailAPIView.as_view()),
]