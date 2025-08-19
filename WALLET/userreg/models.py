from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone_num = models.CharField(max_length=20, default='0987777776')
    date_of_birth = models.DateField(default='2004-11-10')
    address = models.TextField(blank=True, null=True)
    country = CountryField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.email

class KYC(models.Model):
    VERIFICATION_STATUS = [
        ("Pending", "Pending"),
        ("Verified", "Verified"),
        ("Rejected", "Rejected"),
    ]

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="kyc")
    document = models.FileField(upload_to="kyc_documents/", blank=True, null=True)
    address = models.FileField(upload_to="kyc/address/", blank=True, null=True)
    document_type = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default="Pending")
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"KYC for {self.customer.user.username} - {self.status}"

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    role = models.CharField(max_length=100, default="Wallet Admin")  
    can_approve_kyc = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)

    def __str__(self):
        return f"Admin: {self.user.username}"