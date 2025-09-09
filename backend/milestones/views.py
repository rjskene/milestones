from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PaymentMilestoneStructure, PaymentMilestone
from .serializers import (
    PaymentMilestoneStructureSerializer, 
    PaymentMilestoneStructureCreateSerializer,
    PaymentMilestoneSerializer
)


class PaymentMilestoneStructureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Payment Milestone Structures.
    Provides CRUD operations for milestone structures and their milestones.
    """
    queryset = PaymentMilestoneStructure.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PaymentMilestoneStructureCreateSerializer
        return PaymentMilestoneStructureSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PaymentMilestoneViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing individual Payment Milestones.
    """
    queryset = PaymentMilestone.objects.all()
    serializer_class = PaymentMilestoneSerializer
    
    def get_queryset(self):
        """
        Optionally filter milestones by structure ID.
        """
        queryset = PaymentMilestone.objects.all()
        structure_id = self.request.query_params.get('structure_id', None)
        if structure_id is not None:
            queryset = queryset.filter(structure_id=structure_id)
        return queryset