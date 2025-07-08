from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import *


class FacturaCompraViewSet(viewsets.ModelViewSet):
    queryset = FacturasCompras.objects.all()
    serializer_class = FacturaCompraSerializer