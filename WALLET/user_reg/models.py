from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

#using django built in User model with adittional fields
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    #full_name = models.CharField(max_length=30)
    username = models.CharField( max_length=50, unique=True)
    date_of_birth = models.DateField(default='2004-11-12')
    is_superuser = models.BooleanField(default =False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    #authentication using the email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]
    
    objects = CustomUserManager()
    def __str__(self):
        return self.email
class Customer(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10, default='Princess')
    other_name = models.CharField(max_length=20, default='')
    #email = models.EmailField(unique=True)
    #username = models.CharField( max_length=50, unique=True)
    password = models.CharField(max_length=50)
    phone_num= models.CharField(max_length=50, default='0987777776')
    #date_of_birth = models.DateField(default='2004-11-10')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.other_name} {self.last_name}"
    
    # def set_password(self, password):
    #     self.password = make_password(password)
    # def hash(self, *args, **kwargs):
    #     self.password = make_password(self.password)
    #     super().save(*args, **kwargs)
    
