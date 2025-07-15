# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import CustomUser
from .serializer import UserSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated & IsAdminUser]  # Solo admin puede ver todos

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'admin':
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)  # Los demás solo se ven a sí mismos

    def perform_update(self, serializer):
        # Solo admin o el propio usuario pueden modificar
        if self.request.user.rol == 'admin' or self.request.user == self.get_object():
            serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.rol == 'admin':
            instance.delete()
