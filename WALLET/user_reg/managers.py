from django.contrib.auth.models import BaseUserManager

#this file ensures that users are created with username, email and password
#and ensures is_staff and is_superuser is set for admin users
class CustomUserManager(BaseUserManager):
    #creates regular users
    def create_user(self, email, password=None, **extras):
        if not email:
            raise ValueError('Email Required')
       # if not username:
        #    raise ValueError('Username Requied')
        
        email = self.normalize_email(email)
        if isinstance(password, tuple):
            password = password[0]
        user = self.model(email=email, **extras)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #creates superuser
    def create_superuser(self, email, password, **extras):
        extras.setdefault('is_staff', True)
        extras.setdefault('is_superuser', True)
        extras.setdefault('is_active', True)
        
        if extras.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff')
        if extras.get('is_superuser') is not True:
            raise ValueError('Must be a superuser')
        return self.create_user(email, password, **extras)