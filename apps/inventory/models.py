from django.db import models
import uuid as UUID

class Productos(models.Model):
    nombre_producto = models.CharField(max_length=100)
    codigo_producto = models.CharField(max_length=50, unique=True, default='00000000')
    ultimo_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)
    nombre_departamento = models.ForeignKey(
        'Departamentos', 
        on_delete=models.CASCADE, 
        related_name='productos'
    )
    nombre_tipo = models.ForeignKey(
        'TiposProductos', 
        default=None,
        blank=True,
        on_delete=models.CASCADE, 
        related_name='productos'
    )
    unidad_medida = models.ForeignKey(
        'UnidadesMedida', 
        on_delete=models.CASCADE, 
        related_name='productos',
        default=None,
    )
    def proveedores_con_precios(self):
        return self.proveedores_info.select_related('proveedor').all()
    
    def __str__(self):
        return self.nombre_producto
    

class TiposProductos(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_tipo

class Departamentos(models.Model):
    nombre_departamento = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_departamento

class UnidadesMedida(models.Model):
    unidad_medida = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.unidad_medida

class Proveedores(models.Model):
    rut_proveedor = models.CharField(max_length=12, unique=True, primary_key=True, help_text="Formato: XX.XXX.XXX-X")
    razon_social = models.CharField(max_length=200)
    nombre_comercial = models.CharField(max_length=200, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre_comercial or self.razon_social

class Contactos(models.Model):
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, related_name='contactos_proveedor')
    nombre_contacto = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    cargo_contacto = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_contacto} - {self.proveedor.nombre_comercial}"
    
class ProductoProveedor(models.Model):
    producto = models.ForeignKey('Productos', on_delete=models.CASCADE, related_name='proveedores_info')
    proveedor = models.ForeignKey('Proveedores', on_delete=models.CASCADE, related_name='productos_info')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ultima_compra = models.DateField()

    class Meta:
        unique_together = ('producto', 'proveedor')  # Un proveedor puede tener un solo precio por producto (último)

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.proveedor.nombre_comercial or self.proveedor.razon_social}"


class Recetas(models.Model):
    id_receta = models.UUIDField(primary_key=True, default=UUID.uuid4, editable=False)
    id_producto_final = models.ForeignKey(
        Productos, 
        on_delete=models.CASCADE, 
        related_name='recetas_finales'
    )
    id_producto_ingrediente = models.ForeignKey(
        Productos, 
        on_delete=models.CASCADE, 
        related_name='ingredientes_receta'
    )
    cantidad_ingrediente = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id_producto_ingrediente.nombre_producto} → {self.id_producto_final.nombre_producto} ({self.cantidad_ingrediente} {self.id_producto_ingrediente.unidad_medida.unidad_medida})"

    class Meta:
        unique_together = ('id_producto_final', 'id_producto_ingrediente')
