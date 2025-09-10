from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EquipmentSale
from .serializers import EquipmentSaleSerializer, EquipmentSaleScheduleSerializer, MilestoneAssignmentSerializer
from milestones.models import PaymentMilestoneStructure

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
    
    # def create(self, request, *args, **kwargs):
    #     """
    #     Create a new equipment sale.
    #     Handles milestone structure assignment during creation.
    #     """
    #     print (request.data)
    #     serializer = self.get_serializer(data=request.data)
    #     print ('here')
    #     serializer.is_valid(raise_exception=True)
    #     print ('not here')
        # Extract milestone_structure_id if provided
        # milestone_structure_id = serializer.validated_data.pop('milestone_structure_id', None)
        
        # # Create the equipment sale
        # equipment_sale = serializer.save()
        
        # # Assign milestone structure if provided
        # if milestone_structure_id:
        #     try:
        #         milestone_structure = PaymentMilestoneStructure.objects.get(
        #             id=milestone_structure_id
        #         )
        #         equipment_sale.assign_milestone_structure(milestone_structure)
        #     except PaymentMilestoneStructure.DoesNotExist:
        #         # If milestone structure doesn't exist, delete the created sale and return error
        #         equipment_sale.delete()
        #         return Response(
        #             {'milestone_structure_id': ['Milestone structure does not exist']},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        
        # # Return the created sale data
        # response_serializer = EquipmentSaleSerializer(equipment_sale)
        # headers = self.get_success_headers(response_serializer.data)
        # return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
    
    @action(detail=True, methods=['post'])
    def assign_milestone(self, request, pk=None):
        """
        Assign a milestone structure to an equipment sale.
        Only works if the sale doesn't already have a milestone structure.
        """
        equipment_sale = self.get_object()
        
        serializer = MilestoneAssignmentSerializer(
            data=request.data,
            context={'sale': equipment_sale}
        )
        
        if serializer.is_valid():
            try:
                milestone_structure = PaymentMilestoneStructure.objects.get(
                    id=serializer.validated_data['milestone_structure_id']
                )
                equipment_sale.assign_milestone_structure(milestone_structure)
                
                # Return the updated sale data
                sale_serializer = EquipmentSaleSerializer(equipment_sale)
                return Response(sale_serializer.data, status=status.HTTP_200_OK)
                
            except PaymentMilestoneStructure.DoesNotExist:
                return Response(
                    {'detail': 'Milestone structure not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except ValueError as e:
                return Response(
                    {'detail': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)