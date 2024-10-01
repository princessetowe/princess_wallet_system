from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from user_reg.models import CustomUser

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
    username = serializers.CharField()
    password = serializers.CharField(write_only= True)
    
    def validate_login(self, data):
        username = data.get('username')
        password = data.get('password')
        
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Invalid Username')
        
        if not check_password(password, user.password):
            raise serializers.Validation('Invalid Password')