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
from .models import Customer
import requests

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        customer.set_password(validated_data['password'])
        customer.save()
        return customer