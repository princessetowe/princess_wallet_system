# from rest_framework import serializers
# from .models import Customer
# from django.contrib.auth.models import User
# import requests

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'

#     def create(self, validated_data):
#         first_name = validated_data.get('first_name')
#         last_name = validated_data.get('last_name')
#         email = validated_data.get('email')
#         password = validated_data.get('password')
#         date_of_birth = validated_data.get('date_of_birth')
#         accountnum = validated_data.get('accountnum')
#         phone_num = validated_data.get('phone_num')
#         customer = Customer.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password,
#             date_of_birth=date_of_birth,
#             accountnum=accountnum,
#             phone_num=phone_num
#         )
#         return customer
from rest_framework import serializers
from .models import Customer, Wallet
from django.contrib.auth.models import User
from django.db import transaction
import requests

class CustomerSerializer(serializers.ModelSerializer):
    phone_num = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_num', 'date_of_birth', 'address', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
            )
            customer=Customer.objects.create(user=user)
        return user

class WalletSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.user.username', read_only=True)
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ['customer']