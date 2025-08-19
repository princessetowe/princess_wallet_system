from django.db import models
import uuid
from userreg.models import Customer, KYC
from walletapp.models import Wallet

class Transactions(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    CURRENCY_CHOICES = [
    ('NGN', 'Nigerian Naira'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    kyc = models.ForeignKey(KYC, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    transaction_type = models.CharField(max_length=40, choices=TRANSACTION_TYPES, default='Withdrawal')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} from {self.wallet.customer.user.username}'s"