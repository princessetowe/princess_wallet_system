from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  Customer, AdminProfile, KYC

admin.site.register(Customer)
admin.site.register(AdminProfile)
admin.site.register(KYC)