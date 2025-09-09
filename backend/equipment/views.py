from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EquipmentSale
from .serializers import EquipmentSaleSerializer, EquipmentSaleScheduleSerializer


class EquipmentSaleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Equipment Sales.
    Provides CRUD operations for equipment sales and milestone schedules.
    """
    queryset = EquipmentSale.objects.all()
    serializer_class = EquipmentSaleSerializer
    
    def get_serializer_class(self):
        if self.action == 'schedule':
            return EquipmentSaleScheduleSerializer
        return EquipmentSaleSerializer
    
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """
        Get the milestone schedule for a specific equipment sale.
        Returns data formatted for gantt chart visualization.
        """
        equipment_sale = self.get_object()
        serializer = self.get_serializer(equipment_sale)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def schedules(self, request):
        """
        Get milestone schedules for all equipment sales.
        Returns data formatted for gantt chart visualization.
        """
        equipment_sales = self.get_queryset()
        serializer = EquipmentSaleScheduleSerializer(equipment_sales, many=True)
        return Response(serializer.data)