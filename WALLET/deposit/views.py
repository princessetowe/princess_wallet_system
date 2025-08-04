from django.shortcuts import render, redirect
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user_reg.models import Customer, Wallet
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
        
        wallet.balance+amount
        wallet.save()
        
        return Response({"message": f"Deposit of {amount} successful."}, status=status.HTTP_200_OK)