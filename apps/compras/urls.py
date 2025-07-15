# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FacturasComprasView,
    DetalleFacturaCompraView,
    OrdenesCompraView,
    DetalleOrdenCompraView,
)

# -----------------------------
# Router para ViewSets de compras
# -----------------------------

router = DefaultRouter()
router.register(r'facturas', FacturasComprasView)
router.register(r'detalles-factura', DetalleFacturaCompraView)
router.register(r'ordenes', OrdenesCompraView)
router.register(r'detalles-orden', DetalleOrdenCompraView)

urlpatterns = [
    path('', include(router.urls)),
]  # Incluir en urls.py global como path('api/compras/', include('apps.compras.urls'))
