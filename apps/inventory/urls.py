# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoView,
    DepartamentoView,
    TipoProductosView,
    UnidadMedidaView,
    ProveedorView,
    ContactoView,
    ImpuestoEspecificoView,
    ProductoProveedorView,
    KardexView,
    StockActualView
)

# -----------------------------
# Router para ViewSets
# -----------------------------

router = DefaultRouter()
router.register(r'productos', ProductoView)
router.register(r'departamentos', DepartamentoView)
router.register(r'tipos-productos', TipoProductosView)
router.register(r'unidades-medida', UnidadMedidaView)
router.register(r'proveedores', ProveedorView)
router.register(r'contactos', ContactoView)
router.register(r'impuestos-especificos', ImpuestoEspecificoView)
router.register(r'producto-proveedor', ProductoProveedorView)
router.register(r'stock', StockActualView, basename='stock')

# -----------------------------
# URLs adicionales sin router
# -----------------------------

urlpatterns = [
    path('', include(router.urls)),

    # Kardex por producto (con filtro opcional por fecha)
    # Ejemplo: /api/inventory/kardex/5/?fecha_inicio=2025-01-01&fecha_fin=2025-01-31
    path('kardex/<int:producto_id>/', KardexView.as_view(), name='kardex-por-producto'),
]  # Agrega esto en el archivo urls.py de la app inventory
