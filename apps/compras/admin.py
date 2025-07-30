from django.contrib import admin
from .models import *

admin.register(FacturasCompras),
admin.register(OrdenesCompra),
admin.register(DetalleOrdenCompra)

# Register your models here.
