from urllib import response
from wsgiref import headers
from rest_framework import serializers
from .models import Customer, KYC, AdminProfile
from django.contrib.auth.models import User
from django.db import transaction
import random
import string
from django.conf import settings
import requests
from walletapp.models import Wallet
class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    username = serializers.CharField(read_only=True) 


    phone_num = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = Customer
        fields = ['email', 'password', 'username','phone_num', 'date_of_birth', 'address', 'profile_picture', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def generate_unique_username(self, email):
        base_username = email.split("@")[0]
        while True:
            random_digits = ''.join(random.choices(string.digits, k=4))
            username = f"{base_username}{random_digits}"
            if not User.objects.filter(username=username).exists():
                return username

    def validate(self, attrs):
    
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError({"email": "Email is required."})
            
        attrs['username'] = self.generate_unique_username(email)
        return attrs

    def create(self, validated_data, **kwargs):
        with transaction.atomic():
            user_data = {
                'username': validated_data.pop('username'),
                'email': validated_data.pop('email'),
                'password': validated_data.pop('password'),
                'first_name': validated_data.pop('first_name'),
                'last_name': validated_data.pop('last_name'),
            }
            user = User.objects.create_user(**user_data)
            customer_data = {
                'user': user,
                'phone_num': validated_data.pop('phone_num', ''),
                'date_of_birth': validated_data.pop('date_of_birth', None),
                'address': validated_data.pop('address', ''),
                'profile_picture': validated_data.pop('profile_picture', None),
            }
            customer = Customer.objects.create(**customer_data)
        return customer

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = "__all__"
        read_only_fields = ["status", "customer"]

    def create(self, validated_data):
        request = self.context["request"]
        customer = Customer.objects.get(user=request.user)

        kyc, _ = KYC.objects.get_or_create(customer=customer)

        for field, value in validated_data.items():
            setattr(kyc, field, value)

        self.auto_verify(kyc)
        return kyc

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        self.auto_verify(instance)
        return instance
    
    def auto_verify(self, kyc):
        wallet = kyc.customer.wallets.first()
        if not wallet:
            wallet = Wallet.objects.create(customer=kyc.customer, tier="Lord")
        if kyc.bvn_verified and kyc.nin_verified and kyc.location_verified:
            kyc.status = "Verified"
            kyc.customer.is_verified = True
            kyc.customer.save()
            wallet.tier = "King"
            wallet.save()
        elif (kyc.bvn_verified or kyc.nin_verified) and kyc.location_verified:
            kyc.status = "Verified"
            wallet.tier = "Prince"
            wallet.save()
        else:
            kyc.status = "Pending"
            wallet.tier = "Lord"
            wallet.save()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class AdminProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = AdminProfile
        fields = ['id', 'username','email','first_name', 'last_name', 'password', 'role', 'can_approve_kyc', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', "")
        last_name = validated_data.pop('last_name', "")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=False 
        )

        admin_profile = AdminProfile.objects.create(user=user, **validated_data)
        return admin_profile
    
    def to_representation(self, instance):
        return {
            "username": instance.user.username,
            "email": instance.user.email,
            "role": instance.role
        }