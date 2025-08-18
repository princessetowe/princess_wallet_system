from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user_reg.models import  Wallet,Customer
from .serializers import WithdrawSerializer
from rest_framework.exceptions import NotFound
from rest_framework import generics, status, permissions

class WithdrawCreateView(APIView):
    serializer_class = WithdrawSerializer
    permission_classes = (IsAuthenticated,)
    
    WITHDRAWAL_LIMIT = 500000.00 
    def post(self, request, *args, **kwargs):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            customer = user.customer_profile
            wallet = Wallet.objects.get(customer=customer)
        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            raise NotFound("Wallet not found for this user")

        amount = serializer.validated_data['amount']
        if amount > self.WITHDRAWAL_LIMIT:
            return Response({"detail": f"Withdrawal exceeds limit {self.WITHDRAWAL_LIMIT} {wallet.currency}."},status=status.HTTP_400_BAD_REQUEST)

        if wallet.balance < amount:
            return Response({"detail": "Insufficient funds"},status=status.HTTP_400_BAD_REQUEST)

        wallet.balance -= amount
        wallet.save()

        transaction = serializer.save(
            user=customer,
            wallet=wallet,
            transaction_type="Withdrawal",
            status="Processing",
            currency=wallet.currency
        )

        return Response(
            {
                "message": f"Withdrawal of {amount} {wallet.currency} initiated successfully.",
                "transaction_id": transaction.id,
                "new_balance": wallet.balance,
                "status": transaction.status,
            },
            status=status.HTTP_201_CREATED
        )