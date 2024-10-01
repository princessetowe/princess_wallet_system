from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

#for creating new users
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

#for updating new users        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)