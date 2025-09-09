from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import KYC, AdminProfile, Customer
from walletapp.models import Wallet
from .serializers import CustomerSerializer, LoginSerializer, KYCSerializer, AdminProfileSerializer, KYCVerifySerializer
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import EmailVerificationToken
class SignUpAPIView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                customer = serializer.save() 

                user = customer.user
                user.is_active = False
                user.save()

                Wallet.objects.create(customer=customer, balance=0.00)

               #token, created = Token.objects.get_or_create(user=user)
                token = EmailVerificationToken.objects.create(customer=customer)
                verification_url = f"http://127.0.0.1:8000/api/verify-email/{token.token}"
                send_mail(
                    "Confirm your email",
                    f"Hi {user.username}, please confirm your email by clicking this link: {verification_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                return Response({
                    "message": "User registered successfully",
                    "user":{
                        "id":user.id,
                        "username":user.username,
                        "email":user.email,
                    }
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Registration failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active or not user.customer_profile.is_verified:
                return Response({"detail": "Please verify your email before logging in."},status=status.HTTP_400_BAD_REQUEST)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "email": user.email,
                "token": token.key,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail":"Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.auth:
            request.auth.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    
class KYCUploadView(generics.CreateAPIView):
   permission_classes = [IsAuthenticated]

   def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        try:
            kyc = KYC.objects.get(customer=customer)
            serializer = KYCSerializer(data=request.data, context={"request": request})
        except KYC.DoesNotExist:
            serializer = KYCSerializer(data=request.data, context={"request": request})
            
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "KYC submitted successfully", "data": serializer.data}, status=201)
        return Response(serializer.errors, status=400)
   
class KYCVerifyView(generics.UpdateAPIView):
    queryset = KYC.objects.all()
    serializer_class=KYCVerifySerializer
    permission_classes = (IsAdminUser,)

    def update(self, request, *args, **kwargs):
        kyc = self.get_object()
        serializer = self.get_serializer(kyc, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        kyc.status = serializer.validated_data.get("status", kyc.status)
        wallet = Wallet.objects.filter(customer=kyc.customer).first()

        if kyc.status == "Verified":
            kyc.customer.is_verified = True

            if wallet:
                if kyc.document and not kyc.address:
                    wallet.tier="Prince"
                elif kyc.document and kyc.address:

                    wallet.tier = 'King'
                else:
                    wallet.tier = 'Lord'
                wallet.save()

        else:
            kyc.customer.is_verified = False
            if wallet:
                wallet.tier = "Lord"
                wallet.save()
        kyc.customer.save()

        kyc.save()

        return Response(
            {
                "detail": f"KYC {kyc.status}",
                "level": wallet.tier if wallet else None,
                "customer": kyc.customer.user.email
            },
            status=status.HTTP_200_OK
        )
    
class AdminProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'pk'
    
class AdminProfileCreateView(generics.CreateAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only super admins can create new admin accounts.")
        serializer.save()

class VerifyEmailAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token, *args, **kwargs):
        verification_token = get_object_or_404(EmailVerificationToken, token=token)

        if verification_token.is_expired():
            verification_token.delete()
            return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

        customer = verification_token.customer
        user = customer.user
    
        user.is_active = True
        user.save()

        customer.is_verified = True
        customer.save()

        verification_token.delete()

        return Response({
            "status": "success",
            "message": "Email verified successfully!",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
                }
            }, status=status.HTTP_200_OK
        )