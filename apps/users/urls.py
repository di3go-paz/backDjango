# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# -----------------------------
# Router para usuarios
# -----------------------------

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]  # Incluir en urls.py global como: path('api/users/', include('apps.users.urls'))
