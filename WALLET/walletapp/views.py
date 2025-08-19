from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from userreg.models import Customer
from .models import *
from .serializers import  *
from django.db import transaction
from rest_framework.exceptions import NotFound
from rest_framework import generics, status, permissions

class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes =(IsAuthenticated,)

    def get_object(self):
        try:
            customer = self.request.user.customer_profile
            return Wallet.objects.get(customer=customer)
        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            return Response({'detail': "Wallet not found for this user"}, status=status.HTTP_404_NOT_FOUND)

class WalletUpgradeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tier = request.data.get("tier")
        valid_tiers = dict(Wallet.TIER_LIMITS).keys()

        if tier not in valid_tiers:
            return Response({"error": "Invalid wallet tier."}, status=status.HTTP_400_BAD_REQUEST)

        wallet = Wallet.objects.filter(customer=request.user.customer_profile).first()
        if not wallet:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        wallet.tier = tier
        wallet.save()

        return Response(
            {
                "message": f"Wallet upgraded to {tier} successfully.",
                "new_tier": wallet.tier
            },
            status=status.HTTP_200_OK
        )