from rest_framework import serializers
from .models import CustomUser, Customer
from django.contrib.auth.models import User

class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    #password= serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def create(self, data):
        #user= CustomUser.objects.create_user(
            #first_name=data['first_name'],
            #other_name=data['other_name'],
            #last_name=data['last_name'],
        email=data['email'],
        username=data['username'],
            #full_name=data['full_name'],
        password=data['password'],
            #phone_num=data['phone_num'],
        date_of_birth=data['date_of_birth']
        if isinstance(email, tuple):
            email=email[0]
        valid = CustomUser.objects.create_user(
            username=username,
            email=email,
            date_of_birth=date_of_birth
        )
        valid.set_password(password)
        valid.save()
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
    # def create_customer(self, data):
    #     customer=Customer.objects.create_user(
    #     first_name=data.get('first_name', ''),
    #     other_name=data.get('other_name', ''),
    #     last_name=data.get('last_name', ''),
    #     full_name=data['full_name'],
    #     email=data['email'],
    #     username=data['username'],
    #     phone_num=data.get('phone_num', '')
    #     )
    #     return customer
    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        
    
    def validate_user_name(self, username):
        if CustomUser.objects.filter(user_name=username):
            raise serializers.ValidationError('Username not available')
        
    def validate_date_of_birth(self, dob):
        if dob.year > 2006:
            raise serializers.ValidationError('You are not eligible')  
    """def get_full_name(self,obj):
        return f"{obj.first_name} {obj.last_name}"""
        