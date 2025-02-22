from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.conf import settings

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    account_num = models.IntegerField(unique=True, default=1234567098)
    phone_num = models.CharField(max_length=20, default='0987777776')
    date_of_birth = models.DateField(default='2004-11-10')

    def set_password(self, password):
        self.password = make_password(password)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super().save(*args, **kwargs)

