from rest_framework import serializers
from .models import Customer, KYC, AdminProfile
from django.contrib.auth.models import User
from django.db import transaction

class CustomerSerializer(serializers.ModelSerializer):
    phone_num = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_num', 'date_of_birth', 'address', 'profile_picture', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            Customer.objects.create(user=user)
        return user

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = "__all__"
        read_only_fields = ["status", "customer"]

    def create(self, validated_data):
        request = self.context["request"]
        customer = Customer.objects.get(user=request.user)  
        return KYC.objects.create(customer=customer, **validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            kyc = super().update(instance, validated_data)
            wallet = kyc.customer.wallets.first()

            if kyc.document_submitted and wallet.tier == "Lord":
                wallet.tier = "Prince"
                wallet.save()

            if kyc.location_verified and wallet.tier in ["Lord", "Prince"]:
                wallet.tier = "King"
                wallet.save()

        return kyc

class KYCVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ["status"]

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