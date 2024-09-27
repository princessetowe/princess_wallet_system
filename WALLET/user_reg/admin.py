from django.contrib import admin
from user_reg.models import Signup

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'email']