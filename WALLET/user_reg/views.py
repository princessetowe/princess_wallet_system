from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Customer, Wallet, Withdraw
from .serializers import CustomerSerializer, WalletSerializer
from withdraw.serializers import WithdrawSerializer
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

class WithdrawHistoryView(generics.ListAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        try:
            customer = user.customer_profile
            wallet = Wallet.objects.get(customer=customer)

            return Withdraw.objects.filter(wallet=wallet).order_by('-time_made')
        except (Customer.DoesNotExist, Wallet.DoesNotExist):
            return Withdraw.objects.none()

