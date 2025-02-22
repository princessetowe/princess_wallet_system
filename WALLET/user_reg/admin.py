from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['account_num', 'phone_num', 'date_of_birth','last_name', 'first_name', 'email', 'password']
    
