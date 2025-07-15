# models.py
from django.db import models
import uuid as UUID

class Departamentos(models.Model):
    nombre_departamento = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_departamento

class TiposProductos(models.Model):
    nombre_tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tipo

class UnidadesMedida(models.Model):
    unidad_medida = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.unidad_medida

class ImpuestoEspecifico(models.Model):
    nombre_impuesto = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nombre_impuesto} ({self.porcentaje}%)"

class Productos(models.Model):
    nombre_producto = models.CharField(max_length=100)
    codigo_producto = models.CharField(max_length=50, unique=True, default='00000000')
    ultimo_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)

    nombre_departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, related_name='productos')
    nombre_tipo = models.ForeignKey(TiposProductos, default=None, blank=True, on_delete=models.CASCADE, related_name='productos')
    unidad_medida = models.ForeignKey(UnidadesMedida, on_delete=models.CASCADE, related_name='productos', default=None)
    impuesto_especifico = models.ManyToManyField(ImpuestoEspecifico, blank=True)

    def calcular_impuesto_especifico(self, subtotal):
        return sum([
            subtotal * (impuesto.porcentaje / 100)
            for impuesto in self.impuesto_especifico.all()
        ])

    def proveedores_con_precios(self):
        return self.proveedores_info.select_related('proveedor').all()

    def __str__(self):
        return self.nombre_producto

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
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='proveedores_info')
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, related_name='productos_info')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ultima_compra = models.DateField()

    class Meta:
        unique_together = ('producto', 'proveedor')

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.proveedor.nombre_comercial or self.proveedor.razon_social}"

class ProductoProveedorCodigo(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='codigos_proveedor')
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, related_name='codigos_productos')
    codigo_proveedor = models.CharField(max_length=100)

    class Meta:
        unique_together = ('producto', 'proveedor', 'codigo_proveedor')

    def __str__(self):
        return f"{self.codigo_proveedor} ({self.proveedor.nombre_comercial})"

class Recetas(models.Model):
    id_receta = models.UUIDField(primary_key=True, default=UUID.uuid4, editable=False)
    id_producto_final = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='recetas_finales')
    id_producto_ingrediente = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='ingredientes_receta')
    cantidad_ingrediente = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('id_producto_final', 'id_producto_ingrediente')

    def __str__(self):
        return f"{self.id_producto_ingrediente.nombre_producto} → {self.id_producto_final.nombre_producto} ({self.cantidad_ingrediente} {self.id_producto_ingrediente.unidad_medida.unidad_medida})"

class Kardex(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='kardex')
    fecha = models.DateTimeField(auto_now_add=True)

    MOVIMIENTO_CHOICES = [
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('traslado', 'Traslado entre sucursales'),
        ('produccion', 'Entrega a producción'),
        ('ajuste_positivo', 'Ajuste positivo'),
        ('ajuste_negativo', 'Ajuste negativo'),
        ('merma', 'Merma o pérdida'),
    ]
    tipo_movimiento = models.CharField(max_length=20, choices=MOVIMIENTO_CHOICES)
    referencia_id = models.PositiveIntegerField(null=True, blank=True)
    detalle = models.CharField(max_length=255, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['fecha']

class MovimientoInventario(models.Model):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    AJUSTE = 'ajuste'
    TRASLADO = 'traslado'

    TIPOS_MOVIMIENTO = [
        (ENTRADA, 'Entrada'),
        (SALIDA, 'Salida'),
        (AJUSTE, 'Ajuste'),
        (TRASLADO, 'Traslado'),
    ]

    SUBTIPOS_MOVIMIENTO = [
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('ajuste_positivo', 'Ajuste Positivo'),
        ('ajuste_negativo', 'Ajuste Negativo'),
        ('traslado_entrada', 'Traslado Entrada'),
        ('traslado_salida', 'Traslado Salida'),
        ('merma', 'Merma'),
        ('produccion', 'Producción'),
    ]

    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    subtipo = models.CharField(max_length=20, choices=SUBTIPOS_MOVIMIENTO)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    documento_referencia = models.CharField(max_length=100, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fecha.date()} - {self.producto} - {self.tipo} - {self.cantidad}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .utils import actualizar_kardex
        actualizar_kardex(self.producto)

class StockActual(models.Model):
    producto = models.OneToOneField(Productos, on_delete=models.CASCADE, related_name='stock_actual')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre_producto} → {self.cantidad}"
