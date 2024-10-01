from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer
from .forms import  CustomUserChangeForm,CustomUserCreationForm

@admin.register(Customer)
class SignupAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name'] #'full_name', 'username', 'password'
    
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form =CustomUserChangeForm
    list_display = ['email', 'username', 'is_staff', 'is_active']
    fieldsets = (
        (None, 
         {'fields': ('email', 'password')}),
    ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    #('Dates',{'fields':('last_login', 'date_joined')}),
    )
    
    add_fieldsets =(
        (None, {
            'classes': ('wide',),
            'fields': (
                'email','username', 'password','is_staff', 'is_active'
            ),
        }),
    )
    
    search_fields = ('email', 'username')
    ordering = ('email',)
admin.site.register(CustomUser,CustomUserAdmin)