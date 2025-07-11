from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date

class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductosSerializer
    queryset = Productos.objects.all()


class DepartamentoView(viewsets.ModelViewSet):
    serializer_class = DepartamentosSerializer
    queryset = Departamentos.objects.all()

class ProveedorView(viewsets.ModelViewSet):
    serializer_class = ProveedoresSerializer
    queryset = Proveedores.objects.all()
    
class ContactoView(viewsets.ModelViewSet):
    serializer_class = ContactosSerializer
    queryset = Contactos.objects.all()
    
class TipoProductosView(viewsets.ModelViewSet):
    serializer_class = TiposProductosSerializer
    queryset = TiposProductos.objects.all()

class UnidadMedidaView(viewsets.ModelViewSet):
    serializer_class = UnidadesMedidaSerializer
    queryset = UnidadesMedida.objects.all()
    
class ImpuestoEspecificoView(viewsets.ModelViewSet):
    serializer_class = ImpuestosEspecificosSerializer
    queryset = ImpuestoEspecifico.objects.all()

class KardexView(APIView):
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