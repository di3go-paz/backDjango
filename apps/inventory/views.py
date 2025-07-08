from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from .serializer import *

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
