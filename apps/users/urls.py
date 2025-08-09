# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework.authtoken.views import obtain_auth_token


# -----------------------------
# Router para usuarios
# -----------------------------

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api/token-auth/", obtain_auth_token),
]  # Incluir en urls.py global como: path('api/users/', include('apps.users.urls'))
