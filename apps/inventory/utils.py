from decimal import Decimal, ROUND_HALF_UP
from .models import Kardex, MovimientoInventario

def actualizar_kardex(producto):
    movimientos = producto.movimientos.order_by('fecha', 'id')  # orden cronológico estricto
    saldo_cantidad = Decimal('0.00')
    saldo_valor = Decimal('0.00')

    # Eliminar el kardex anterior
    producto.kardex.all().delete()

    for mov in movimientos:
        cantidad = mov.cantidad
        costo_unitario = mov.costo_unitario

        if mov.tipo == MovimientoInventario.ENTRADA:
            saldo_cantidad += cantidad
            saldo_valor += cantidad * costo_unitario
        elif mov.tipo in [MovimientoInventario.SALIDA, MovimientoInventario.AJUSTE, MovimientoInventario.TRASLADO]:
            saldo_cantidad -= cantidad
            saldo_valor -= cantidad * costo_unitario

        # Redondeo
        saldo_cantidad = saldo_cantidad.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        saldo_valor = saldo_valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        Kardex.objects.create(
            producto=producto,
            fecha=mov.fecha,
            tipo_movimiento=mov.subtipo,
            referencia_id=mov.id,
            detalle=mov.observacion or '',
            cantidad=cantidad,
            costo_unitario=costo_unitario,
            saldo_cantidad=saldo_cantidad,
            saldo_valor=saldo_valor
        )
