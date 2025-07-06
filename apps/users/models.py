from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None,rol='administrador', **extra_fields):
        if not username:
            raise ValueError('nombre de usuario obligatorio obligatorio')
        user = self.model(username=username, rol=rol, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username,password,rol='admin', **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=50, choices = [
        ('admin', 'Administrador'),
        ('vendedor','vendedor'),
        ('caja','caja')
    ], default='vendedor')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login_date = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
