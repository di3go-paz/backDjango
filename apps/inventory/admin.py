from django.contrib import admin
from .models import *

admin.site.register(Productos)
admin.site.register(Departamentos)
admin.site.register(TiposProductos)
admin.site.register(Proveedores)
admin.site.register(Contactos)
admin.site.register(UnidadesMedida)
admin.site.register(ProductoProveedor)
admin.site.register(ImpuestoEspecifico)

