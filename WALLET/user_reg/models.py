from django.db import models

class Signup(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10, default='Princess')
    other_name = models.CharField(max_length=20, default='')
    email = models.EmailField(unique=True, blank=True)
    username = models.CharField( max_length=50, unique=True)
    password = models.CharField(max_length=50)
    phone_num= models.CharField(max_length=50)
    date_of_birth = models.DateField()
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.other_name} {self.last_name}"
    
