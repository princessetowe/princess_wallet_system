from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user_reg.models import Withdraw, Wallet
from .serializers import WithdrawSerializer
from rest_framework import generics, status, permissions

class WithdrawCreateView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        user = self.request.user
        try:
            customer = user.customer_profile
            wallet = Wallet.objects.get(customer=customer)
        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            return Response({"detail": "Wallet not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        amount = serializer.validated_data['amount']
        if wallet.balance >= amount:
            wallet.balance -= amount
            wallet.save()
            serializer.save(wallet=wallet, status='Processing')
        else:
            return Response({"detail":"Insufficient Funds"}, status=status.HTTP_400_BAD_REQUEST)
