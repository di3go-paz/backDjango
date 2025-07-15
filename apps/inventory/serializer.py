# serializers.py
from rest_framework import serializers
from .models import *

class DepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamentos
        fields = '__all__'

class TiposProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposProductos
        fields = '__all__'

class UnidadesMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadesMedida
        fields = '__all__'

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = '__all__'

class ContactosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactos
        fields = '__all__'

class ImpuestosEspecificosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpuestoEspecifico
        fields = '__all__'


class ProductosSerializer(serializers.ModelSerializer):
    nombre_departamento = DepartamentosSerializer(read_only=True)
    nombre_tipo = TiposProductosSerializer(read_only=True)
    unidad_medida = UnidadesMedidaSerializer(read_only=True)
    impuesto_especifico = ImpuestosEspecificosSerializer(many=True, read_only=True)
    proveedores_info = serializers.SerializerMethodField()

    class Meta:
        model = Productos
        fields = '__all__'

    def get_proveedores_info(self, obj):
        return [
            {
                "precio_compra": pp.precio_compra,
                "fecha_ultima_compra": pp.fecha_ultima_compra,
                "proveedor": {
                    "rut_proveedor": pp.proveedor.rut_proveedor,
                    "nombre_comercial": pp.proveedor.nombre_comercial,
                    "razon_social": pp.proveedor.razon_social,
                },
            }
            for pp in obj.proveedores_info.all()
        ]
class ProductoProveedorSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(read_only=True)
    proveedor = ProveedoresSerializer(read_only=True)

    class Meta:
        model = ProductoProveedor
        fields = '__all__'
        read_only_fields = ('producto', 'proveedor')

class ProductosWriteSerializer(serializers.ModelSerializer):
    impuesto_especifico = serializers.PrimaryKeyRelatedField(queryset=ImpuestoEspecifico.objects.all(), many=True)

    class Meta:
        model = Productos
        fields = '__all__'

class KardexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kardex
        fields = '__all__'

class StockActualSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='producto.nombre_producto', read_only=True)
    codigo_producto = serializers.CharField(source='producto.codigo_producto', read_only=True)

    class Meta:
        model = StockActual
        fields = ['id', 'producto', 'nombre_producto', 'codigo_producto', 'cantidad', 'actualizado_en']
