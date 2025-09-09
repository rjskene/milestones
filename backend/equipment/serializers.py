from rest_framework import serializers
from .models import EquipmentSale
from milestones.serializers import PaymentMilestoneStructureSerializer


class EquipmentSaleSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentSale objects."""
    milestone_structure = PaymentMilestoneStructureSerializer(read_only=True)
    milestone_structure_id = serializers.IntegerField(write_only=True)
    unit_price = serializers.ReadOnlyField()
    
    class Meta:
        model = EquipmentSale
        fields = [
            'id', 'name', 'vendor', 'quantity', 'total_amount', 
            'milestone_structure', 'milestone_structure_id', 
            'project_start_date', 'unit_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EquipmentSaleScheduleSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentSale with milestone schedule data."""
    milestone_structure = PaymentMilestoneStructureSerializer(read_only=True)
    unit_price = serializers.ReadOnlyField()
    milestone_schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentSale
        fields = [
            'id', 'name', 'vendor', 'quantity', 'total_amount',
            'milestone_structure', 'project_start_date', 'unit_price',
            'milestone_schedule', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_milestone_schedule(self, obj):
        """Get the milestone schedule data for gantt chart."""
        return obj.get_milestone_schedule()