from rest_framework import serializers
# from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)