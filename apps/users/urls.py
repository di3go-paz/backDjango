# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import CustomAuthToken
from rest_framework.authtoken.views import obtain_auth_token


# -----------------------------
# Router para usuarios
# -----------------------------

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api/token-auth/", CustomAuthToken.as_view(), name="token-auth"),  # Ruta para obtener token con rol
]  # Incluir en urls.py global como: path('/users/', include('apps.users.urls'))
