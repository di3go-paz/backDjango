# serializers.py
from rest_framework import serializers
from .models import *
from apps.inventory.serializer import ProveedoresSerializer, ProductosSerializer

# -----------------------------
# Lectura: Detalles y cabeceras
# -----------------------------

class DetalleFacturaCompraSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(read_only=True)

    class Meta:
        model = DetalleFacturaCompra
        fields = '__all__'

class FacturasComprasSerializer(serializers.ModelSerializer):
    proveedor = ProveedoresSerializer(read_only=True)
    detalles = DetalleFacturaCompraSerializer(many=True, read_only=True)

    class Meta:
        model = FacturasCompras
        fields = '__all__'

class DetalleOrdenCompraSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(read_only=True)

    class Meta:
        model = DetalleOrdenCompra
        fields = '__all__'

class OrdenesCompraSerializer(serializers.ModelSerializer):
    proveedor = ProveedoresSerializer(read_only=True)
    detalles = DetalleOrdenCompraSerializer(many=True, read_only=True)

    class Meta:
        model = OrdenesCompra
        fields = '__all__'

# -----------------------------
# Escritura: solo IDs
# -----------------------------

class DetalleFacturaCompraWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFacturaCompra
        fields = '__all__'

class FacturasComprasWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturasCompras
        fields = '__all__'

class DetalleOrdenCompraWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrdenCompra
        fields = '__all__'

class OrdenesCompraWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenesCompra
        fields = '__all__'
