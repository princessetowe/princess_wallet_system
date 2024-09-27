from rest_framework import serializers
from user_reg.models import Signup

class SignupSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    class Meta:
        model = Signup
        fields = ['first_name', 'other_name','last_name','email', 'username', 'password', 'phone_num', 'date_of_birth', 'full_name']
      
    def validate_email(self, email):
        if Signup.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        
    
    def validate_user_name(self, username):
        if Signup.objects.filter(user_name=username):
            raise serializers.ValidationError('Username not available')
        
    def validate_date_of_birth(self, dob):
        if dob.year > 2006:
            raise serializers.ValidationError('You are not eligible')
        
    """def get_full_name(self,obj):
        return f"{obj.first_name} {obj.last_name}"""
        