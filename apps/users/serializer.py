# serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'rol', 'is_active', 'last_login_date']
        read_only_fields = ['id', 'is_active', 'last_login_date']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'rol']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
