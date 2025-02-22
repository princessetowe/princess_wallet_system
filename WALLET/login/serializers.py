from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from user_reg.models import Customer

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email', 'password']
    email = serializers.CharField()
    password = serializers.CharField(write_only= True)
    
    def validate_login(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError('Invalid Email')
        
        if not check_password(password, user.password):
            raise serializers.Validation('Invalid Password')