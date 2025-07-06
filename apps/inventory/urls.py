from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'productos', ProductoView, basename='productos')
router.register(r'departamentos', DepartamentoView, basename='departamentos')
router.register(r'proveedores', ProveedorView, basename='proveedores')
router.register(r'contactos', ContactoView, basename='contactos')
router.register(r'tipos_productos', TipoProductosView, basename='tipos_productos')
router.register(r'unidad_medida', UnidadMedidaView, basename='unidad_medida')

urlpatterns = [
    path('api/v1/', include(router.urls))
    
]

