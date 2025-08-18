from rest_framework import status
from rest_framework.response import Response
from user_reg.models import Customer, Wallet, Transactions
from .serializers import DepositSerializer
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

class DepositCreateView(APIView):
    serializer_class = DepositSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        user = self.request.user
        try:
            customer = user.customer_profile
            wallet = Wallet.objects.get(customer=customer)
        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            raise status.HTTP_404_NOT_FOUND("Wallet not found for this user")
        
        tier_limit = Wallet.TIER_LIMITS.get(wallet.tier)
        if tier_limit is not None and amount > tier_limit:
            return Response({"error": f"Deposit exceeds the {wallet.tier} wallet limit of {tier_limit} {wallet.currency}."},
                status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            wallet.balance+=amount
            wallet.save()

            transaction_obj = Transactions.objects.create(
                user=customer,
                wallet=wallet,
                transaction_type="Deposit",
                amount=amount,
                currency=wallet.currency,
                status="Successful"
            )

        return Response(
            {
                "message": f"Deposit of {amount} {wallet.currency} successful.",
                "transaction_id": transaction_obj.id,
                "new_balance": wallet.balance,
                "wallet_tier": wallet.tier,
            },
            status=status.HTTP_200_OK
        )