# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'admin'

class EsCompras(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'compras'

class EsInventario(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'inventario'

class EsCaja(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'caja'

class EsConsulta(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'consulta'

class SoloLectura(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in SAFE_METHODS
