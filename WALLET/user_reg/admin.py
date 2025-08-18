from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  Customer, Wallet, Transactions

admin.site.register(Customer)
admin.site.register(Wallet)
admin.site.register(Transactions)

    
