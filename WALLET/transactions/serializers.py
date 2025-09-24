from rest_framework import serializers
from .models import Transactions
from walletapp.models import Wallet
from userreg.models import Customer
import requests
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
import string
import secrets
import uuid

class TransactionSerializer(serializers.ModelSerializer):
    kyc_status = serializers.CharField(source="kyc.verification_status", read_only=True)
    class Meta:
        model = Transactions
        fields = '__all__'


def generate_reference(length=10):
    return f"acv_{uuid.uuid4()}"[:50]

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["amount"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        customer = user.customer_profile
        wallet = Wallet.objects.get(customer=customer)

        amount = attrs.get("amount")

        if amount is None:
            raise serializers.ValidationError({"amount": "This field is required."})

        try:
            amount = Decimal(str(amount))
        except (ValueError, TypeError):
            raise serializers.ValidationError({"amount": "Amount must be a valid number."})

        if amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be positive"})

        if wallet.balance < amount:
            raise serializers.ValidationError({"balance": "Insufficient funds"})

        tier_limit = wallet.TIER_LIMITS.get(wallet.tier, 0)
        if amount > tier_limit:
            raise serializers.ValidationError(
                {"limit": f"Withdrawals exceed {wallet.tier} limit of {tier_limit}"}
            )

        attrs["wallet"] = wallet
        attrs["customer"] = customer
        attrs["amount"] = amount
        return attrs

    def create(self, validated_data):
        wallet = validated_data.get("wallet")
        customer = validated_data.get("customer")
        amount = validated_data.get("amount")

        wallet.balance -= amount
        wallet.save()

        reference = generate_reference()

        transaction = Transactions.objects.create(
            user=customer,
            wallet=wallet,
            amount=amount,
            transaction_type="Withdrawal",
            status="Success",
            currency=wallet.currency,
            reference=reference,
        )
        return {
            "transaction_id": transaction.id,
            "reference": transaction.reference,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "status": transaction.status,
        }

    
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["amount"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
    
       
        customer = user.customer_profile 
        wallet = Wallet.objects.get(customer=customer)
  
        amount = attrs.get("amount")

        if amount is None:
            raise serializers.ValidationError({"amount": "This field is required."})

        try:
            amount = Decimal(str(amount))
        except (ValueError, TypeError):
            raise serializers.ValidationError({"amount": "Amount must be a valid number."})

        if amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be positive"})

        tier_limit = wallet.TIER_LIMITS.get(wallet.tier, 0)
        if wallet.balance + amount > tier_limit:
            raise serializers.ValidationError(
                {"limit": f"Deposit exceeds {wallet.tier} limit of {tier_limit}"}
            )

        attrs["wallet"] = wallet
        attrs["customer"] = customer
        attrs["amount"] = amount
        return attrs

    def create(self, validated_data):
        wallet = validated_data.get("wallet")
        customer = validated_data.get("customer")
        amount = validated_data.get("amount")

        #paystack

        url = 'https://api.paystack.co/transaction/initialize'

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
            }
        
        data = {
            "email": customer.user.email,
            "amount": int(amount * 100),
            "currency": wallet.currency,
        }


        r = requests.post(url, headers=headers, json=data)
        response = r.json()
        if not response.get("status"):
            raise serializers.ValidationError({"paystack": "Failed to initialize deposit"})

        paystack_data = response["data"]
        # wallet.balance += amount
        # wallet.save()

        transaction = Transactions.objects.create(
            user=customer,
            wallet=wallet,
            amount=amount,
            transaction_type="Deposit",
            status="Processing",
            currency=wallet.currency,
            reference=paystack_data["reference"],
        )
        transaction.payment_url = response["data"]["authorization_url"]
        return {
            "transaction_id": transaction.id,
            "reference": paystack_data["reference"],
            "authorization_url": paystack_data["authorization_url"],
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "status": transaction.status,
        }

class TransferSerializer(serializers.ModelSerializer):
    recipient_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Transactions
        fields = ["amount", "recipient_email"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        customer = user.customer_profile
        wallet = Wallet.objects.get(customer=customer)

        amount = attrs.get("amount")
        recipient_email = attrs.get("recipient_email")

        if amount is None:
            raise serializers.ValidationError({"amount": "This field is required."})

        try:
            amount = Decimal(str(amount))
        except (ValueError, TypeError):
            raise serializers.ValidationError({"amount": "Amount must be a valid number."})

        if amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be positive"})

        if wallet.balance < amount:
            raise serializers.ValidationError({"balance": "Insufficient funds"})

        tier_limit = wallet.TIER_LIMITS.get(wallet.tier, 0)
        if amount > tier_limit:
            raise serializers.ValidationError(
                {"limit": f"Transfer exceeds {wallet.tier} limit of {tier_limit}"}
            )

        try:
            recipient_user = Customer.objects.get(user__email=recipient_email)
            recipient_wallet = Wallet.objects.get(customer=recipient_user)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({"recipient_email": "Recipient not found"})
        except Wallet.DoesNotExist:
            raise serializers.ValidationError({"recipient_email": "Recipient wallet not found"})

        if recipient_user == customer:
            raise serializers.ValidationError({"recipient_email": "Cannot transfer to self"})

        attrs["wallet"] = wallet
        attrs["customer"] = customer
        attrs["amount"] = amount
        attrs["recipient_wallet"] = recipient_wallet
        return attrs

    def create(self, validated_data):
        wallet = validated_data.get("wallet")
        customer = validated_data.get("customer")
        amount = validated_data.get("amount")
        recipient_wallet = validated_data.get("recipient_wallet")

        from django.db import transaction
        with transaction.atomic():
            wallet.balance -= amount
            wallet.save()

            recipient_wallet.balance += amount
            recipient_wallet.save()

            reference = generate_reference()

            transaction = Transactions.objects.create(
                user=customer,
                wallet=wallet,
                amount=amount,
                transaction_type="Transfer",
                status="Success",
                currency=wallet.currency,
                reference=reference,
            )

            return {
            "transaction_id": transaction.id,
            "reference": transaction.reference,
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "status": transaction.status,
        }