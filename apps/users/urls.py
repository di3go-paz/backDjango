from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import UserView

router = DefaultRouter()
router.register(r'users', UserView,basename='users')

urlpatterns = [
    path('api/v1/', include(router.urls))
]
