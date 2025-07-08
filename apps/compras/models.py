from django.db import models
from apps.inventory.models import Proveedores
from apps.inventory.models import Productos


class FacturasCompras(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(
        Proveedores,
        on_delete=models.CASCADE,
        )
    valor_neto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    iva = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    impuestos_especificos = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    def calcular_total(self):
        detalles = self.detalles.all()
        self.valor_neto = sum([d.subtotal for d in detalles])
        self.impuestos_especificos = sum([d.impuestos_especificos for d in detalles])
        self.iva = round(self.valor_neto * 0.19, 2)
        self.total = self.valor_neto + self.iva + self.impuestos_especificos
        self.save()
        
class DetalleFacturaCompra(models.Model):
    factura = models.ForeignKey(
        FacturasCompras,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        related_name='detalles_factura'
    )
    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    impuestos_especificos = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        if hasattr(self.producto, 'calcular_impuesto_especifico'):
            self.impuestos_especificos = self.producto.calcular_impuesto_especifico(self.subtotal)
        else:
            self.impuestos_especificos = 0
        super().save(*args, **kwargs)
        
class OrdenesCompra(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(
        Proveedores,
        on_delete=models.CASCADE,
        related_name='ordenes_compra'
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    
    def calcular_total(self):
        detalles = self.detalles.all()
        self.total = sum([d.subtotal for d in detalles])
        self.save()
        
class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(
        OrdenesCompra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        related_name='detalles_orden_compra'
    )
    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)