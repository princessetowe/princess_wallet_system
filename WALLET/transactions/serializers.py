from rest_framework import serializers
from .models import Transactions
from walletapp.models import Wallet
from userreg.models import Customer
import requests

class TransactionSerializer(serializers.ModelSerializer):
    kyc_status = serializers.CharField(source="kyc.verification_status", read_only=True)
    class Meta:
        model = Transactions
        fields = '__all__'

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["amount"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        customer = user.customer_profile
        wallet = Wallet.objects.get(customer=customer)

        amount = attrs["amount"]

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
        return attrs

    def create(self, validated_data):
        wallet = validated_data.get("wallet")
        customer = validated_data.get("customer")
        amount = validated_data.get("amount")

        wallet.balance -= amount
        wallet.save()

        transaction = Transactions.objects.create(
            user=customer,
            wallet=wallet,
            amount=amount,
            transaction_type="Withdrawal",
            status="Processing",
            currency=wallet.currency,
        )
        return transaction
    
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["amount"]

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
    
       
        customer = user.customer_profile
        wallet = Wallet.objects.get(customer=customer)
  
        amount = attrs["amount"]

        if amount <= 0:
            raise serializers.ValidationError({"amount": "Amount must be positive"})

        tier_limit = wallet.TIER_LIMITS.get(wallet.tier, 0)
        if wallet.balance + amount > tier_limit:
            raise serializers.ValidationError(
                {"limit": f"Deposit exceeds {wallet.tier} limit of {tier_limit}"}
            )

        attrs["wallet"] = wallet
        attrs["customer"] = customer
        return attrs

    def create(self, validated_data):
        wallet = validated_data.get("wallet")
        customer = validated_data.get("customer")
        amount = validated_data.get("amount")

        wallet.balance += amount
        wallet.save()

        transaction = Transactions.objects.create(
            user=customer,
            wallet=wallet,
            amount=amount,
            transaction_type="Deposit",
            status="Successful",
            currency=wallet.currency,
        )
        return transaction
