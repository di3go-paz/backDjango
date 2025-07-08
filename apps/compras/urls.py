from rest_framework import serializers
from .views import *

router = DefaultRouter()
router.register(r'facturas', FacturaCompraViewSet)

urlpatterns = router.urls

