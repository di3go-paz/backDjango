from rest_framework import viewsets
from apps.users.serializer import UserSerializer
from .models import CustomUser

# Create your views here.
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
