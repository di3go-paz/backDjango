from rest_framework import serializers
from .models import *
from apps.inventory.serializer import *

class FacturaCompraSerializer(serializers.ModelSerializer):
    detalles = serializers.SerializerMethodField()

    class Meta: 
        model = FacturasCompras
        fields = '__all__'

    def get_detalles(self, obj):
        return DetalleFacturaCompraSerializer(obj.detalles.all(), many=True).data

class DetalleFacturaCompraSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(read_only=True)

    class Meta:
        model = DetalleFacturaCompra
        fields = '__all__'
        read_only_fields = ('producto',)
    
class OrdenCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenesCompra
        fields = '__all__'
        
class DetalleOrdenCompraSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(read_only=True)

    class Meta:
        model = DetalleOrdenCompra
        fields = '__all__'
        read_only_fields = ('producto',)