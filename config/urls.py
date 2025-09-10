
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect




urlpatterns = [
    path('', lambda request: redirect('admin:index')),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/compras/', include('apps.compras.urls')),
] 