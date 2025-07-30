# models.py
from django.db import models
from apps.inventory.models import Proveedores, Productos, MovimientoInventario

class OrdenesCompra(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, related_name='ordenes_compra')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('parcial', 'Recepción parcial'),
        ('completa', 'Recepción completa'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calcular_total(self):
        detalles = self.detalles.all()
        self.total = sum([d.subtotal for d in detalles])
        self.save()

    def __str__(self):
        return f"Orden #{self.id} - {self.proveedor}"

class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(OrdenesCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='detalles_orden_compra')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

class FacturasCompras(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    orden_origen = models.ForeignKey(OrdenesCompra, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas_generadas')

    valor_neto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    impuestos_especificos = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('recibida', 'Recibida'),
        ('anulada', 'Anulada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calcular_total(self):
        detalles = self.detalles.all()
        self.valor_neto = sum([d.subtotal for d in detalles])
        self.impuestos_especificos = sum([d.impuestos_especificos for d in detalles])
        self.iva = round(self.valor_neto * 0.19, 2)
        self.total = self.valor_neto + self.iva + self.impuestos_especificos
        self.save()

    def save(self, *args, **kwargs):
        estado_anterior = None
        if self.pk:
            estado_anterior = FacturasCompras.objects.get(pk=self.pk).estado

        super().save(*args, **kwargs)

        # Si cambia a "recibida", generar movimientos de inventario
        if self.estado == 'recibida' and estado_anterior != 'recibida':
            for detalle in self.detalles.all():
                MovimientoInventario.objects.create(
                    producto=detalle.producto,
                    tipo='entrada',
                    subtipo='compra',
                    cantidad=detalle.cantidad,
                    costo_unitario=detalle.precio_unitario,
                    documento_referencia=f"Factura #{self.id}",
                    observacion="Ingreso automático por factura recibida"
                )

    def __str__(self):
        return f"Factura #{self.id} - {self.proveedor}"

class DetalleFacturaCompra(models.Model):
    factura = models.ForeignKey(FacturasCompras, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='detalles_factura')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    impuestos_especificos = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        if hasattr(self.producto, 'calcular_impuesto_especifico'):
            self.impuestos_especificos = self.producto.calcular_impuesto_especifico(self.subtotal)
        else:
            self.impuestos_especificos = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

