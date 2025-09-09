from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentSaleViewSet

router = DefaultRouter()
router.register(r'sales', EquipmentSaleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


