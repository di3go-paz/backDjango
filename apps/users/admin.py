from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin): 
    model = CustomUser
    list_display =('username', 'rol', 'is_active', 'last_login_date')
    list_filter = ('rol', 'is_active')
    fieldsets = (
        (None, {'fields':('username', 'password')}),
        ('Informacion adicional', {'fields':('rol', 'is_active', 'last_login_date')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('username','password1', 'password2', 'rol', 'is_active')}
         ),
        
    )
    search_fields = ('username',)
    ordering = ('username',)
    
admin.site.register(CustomUser, CustomUserAdmin)
    
# Register your models here.
