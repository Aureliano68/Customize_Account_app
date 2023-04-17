from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import CustomerUser


# ---------------------------------------------------------------------------------------------------
class CustomUserAdmin(UserAdmin):
    form = UserchangeForm
    add_form = UsercreateForm
    
    list_display=('mobile_number','email','name','family','gender','is_active','is_admin')
    list_filter=['is_active','is_admin']
    
    fieldsets = (
        (None, {"fields": ("mobile_number", "password")}),
        (("Personal info"), {"fields": ("name", "family", "gender")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    'is_admin',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                   
                ),
            },
        ),
       
    )
    add_fieldsets = (
        (None, {"fields": ('mobile_number','email','name','family','gender','password1','password2')}),
    )
    
    search_fields=['mobile_number']
    ordering=['mobile_number']
    filter_horizontal=( 'groups','user_permissions')
                    

admin.site.register(CustomerUser,CustomUserAdmin)


# ---------------------------------------------------------------------------------------------------
