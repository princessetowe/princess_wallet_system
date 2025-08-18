from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

User = get_user_model()
CURRENCY_CHOICES = [
    ('NGN', 'Nigerian Naira'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
]


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

class Wallet(models.Model):
    WALLET_TIER_CHOICES = [
        ('Lord', 'Lord'),
        ('Prince', 'Prince'),
        ('King', 'King'),
    ]
    TIER_LIMITS = {
        'Lord': 50000.00,
        'Prince': 200000.00,
        'King': 500000.00,
    }

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    tier = models.CharField(max_length=20, choices=WALLET_TIER_CHOICES, default="Lord")
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet for {self.customer.user.username}"

class Transactions(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    ]
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=40, choices=TRANSACTION_TYPES, default='Withdrawal')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    status = models.CharField(max_length=50, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} from {self.wallet.customer.user.username}'s"
