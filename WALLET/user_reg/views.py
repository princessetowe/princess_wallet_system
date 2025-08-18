from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Customer, Wallet, Transactions
from .serializers import CustomerSerializer, WalletSerializer, TransactionSerializer
from rest_framework.authtoken.models import Token
from django.db import transaction
# Create your views here.
class SignUpAPIView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                user = serializer.save()
                customer = user.customer_profile

                Wallet.objects.create(customer=customer, balance=0.00)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "User registered successfully",
                    "user":{
                        "id":user.id,
                        "username":user.username,
                        "email":user.email,
                    },
                    "token": token.key,
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Registration failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes =(IsAuthenticated,)

    def get_object(self):
        try:
            customer = self.request.user.customer_profile
            return Wallet.objects.get(customer=customer)
        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            return Response({'detail': "Wallet not found for this user"}, status=status.HTTP_404_NOT_FOUND)

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