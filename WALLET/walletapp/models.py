from django.db import models
from userreg.models import Customer
from django.utils import timezone

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

    CURRENCY_CHOICES = [
    ('NGN', 'Nigerian Naira'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    tier = models.CharField(max_length=20, choices=WALLET_TIER_CHOICES, default="Lord")
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet for {self.customer.user.username}"
    
    def same_kyc(self):
        mapped_tier = self.customer.get_wallet_tier()
        if self.tier != mapped_tier:
            self.tier = mapped_tier
            self.save()

    def can_fund(self, amount):
        self.same_kyc()
        limit = self.TIER_LIMITS.get(self.tier, 0)
        return (self.balance + amount) <= limit