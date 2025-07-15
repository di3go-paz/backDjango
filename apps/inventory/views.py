# views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from .models import *
from .serializer import *

# -----------------------------
# ViewSets CRUD principales
# -----------------------------

class ProductoView(viewsets.ModelViewSet):
    """
    Vista para productos.
    - Usa serializer de solo lectura para GET.
    - Usa serializer de escritura para POST, PUT, PATCH.
    """
    queryset = Productos.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductosWriteSerializer
        return ProductosSerializer

class DepartamentoView(viewsets.ModelViewSet):
    queryset = Departamentos.objects.all()
    serializer_class = DepartamentosSerializer

class TipoProductosView(viewsets.ModelViewSet):
    queryset = TiposProductos.objects.all()
    serializer_class = TiposProductosSerializer

class UnidadMedidaView(viewsets.ModelViewSet):
    queryset = UnidadesMedida.objects.all()
    serializer_class = UnidadesMedidaSerializer

class ProveedorView(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedoresSerializer

class ContactoView(viewsets.ModelViewSet):
    queryset = Contactos.objects.all()
    serializer_class = ContactosSerializer

class ImpuestoEspecificoView(viewsets.ModelViewSet):
    queryset = ImpuestoEspecifico.objects.all()
    serializer_class = ImpuestosEspecificosSerializer

class ProductoProveedorView(viewsets.ModelViewSet):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductoProveedorSerializer

# -----------------------------
# Vista para Kardex filtrado
# -----------------------------

class KardexView(APIView):
    """
    Devuelve el historial de movimientos (kardex) de un producto específico.
    Permite filtrar por fecha de inicio y fin con query params.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, producto_id):
        fecha_inicio = parse_date(request.GET.get('fecha_inicio')) if request.GET.get('fecha_inicio') else None
        fecha_fin = parse_date(request.GET.get('fecha_fin')) if request.GET.get('fecha_fin') else None

        kardex_qs = Kardex.objects.filter(producto_id=producto_id)
        if fecha_inicio:
            kardex_qs = kardex_qs.filter(fecha__date__gte=fecha_inicio)
        if fecha_fin:
            kardex_qs = kardex_qs.filter(fecha__date__lte=fecha_fin)

        kardex_qs = kardex_qs.order_by('fecha')
        serializer = KardexSerializer(kardex_qs, many=True)
        return Response(serializer.data)

# -----------------------------
# Vista para stock actual
# -----------------------------

class StockActualView(viewsets.ReadOnlyModelViewSet):
    """
    Solo permite lectura del stock actual por producto.
    Útil para dashboards o vistas rápidas.
    """
    queryset = StockActual.objects.select_related('producto')
    serializer_class = StockActualSerializer
