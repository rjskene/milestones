from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMilestoneStructureViewSet, PaymentMilestoneViewSet

router = DefaultRouter()
router.register(r'structures', PaymentMilestoneStructureViewSet)
router.register(r'milestones', PaymentMilestoneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


