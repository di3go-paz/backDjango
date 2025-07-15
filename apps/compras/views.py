# views.py
from rest_framework import viewsets
from .models import *
from .serializer import *

# -----------------------------
# ViewSets para facturas y órdenes
# -----------------------------

class FacturasComprasView(viewsets.ModelViewSet):
    """
    Vista CRUD para facturas de compra.
    Utiliza serializers diferenciados para lectura y escritura.
    """
    queryset = FacturasCompras.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FacturasComprasWriteSerializer
        return FacturasComprasSerializer

class DetalleFacturaCompraView(viewsets.ModelViewSet):
    queryset = DetalleFacturaCompra.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DetalleFacturaCompraWriteSerializer
        return DetalleFacturaCompraSerializer

class OrdenesCompraView(viewsets.ModelViewSet):
    """
    Vista CRUD para órdenes de compra.
    Utiliza serializers diferenciados para lectura y escritura.
    """
    queryset = OrdenesCompra.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrdenesCompraWriteSerializer
        return OrdenesCompraSerializer

class DetalleOrdenCompraView(viewsets.ModelViewSet):
    queryset = DetalleOrdenCompra.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DetalleOrdenCompraWriteSerializer
        return DetalleOrdenCompraSerializer
