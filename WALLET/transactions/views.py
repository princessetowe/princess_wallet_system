from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from userreg.models import Customer
from .models import *
from .serializers import  *
from django.db import transaction
from rest_framework.exceptions import NotFound
from rest_framework import generics, status, permissions

class WithdrawCreateView(APIView):
    serializer_class = WithdrawSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
          
        return Response(
            {
                "message": f"Success",
                **transaction
            },
            status=status.HTTP_201_CREATED
        )
    
class DepositCreateView(APIView):
    serializer_class = DepositSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
    
        return Response(
            {
                "message": "Deposit initialized.",
                **transaction
            },
            status=status.HTTP_200_OK
        )
    
class TransferCreateView(APIView):
    serializer_class = TransferSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        return Response(
            {
                "message":f"Success",
                **transaction
            },
            status=status.HTTP_201_CREATED
        )
    
class TransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        try:
            customer = user.customer_profile
            wallet = Wallet.objects.get(customer=customer)

            return Transactions.objects.filter(wallet=wallet).order_by('-created_at')
        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            return Transactions.objects.none()