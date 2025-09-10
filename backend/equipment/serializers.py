from rest_framework import serializers
from .models import EquipmentSale
from milestones.serializers import PaymentMilestoneStructureSerializer


class NullableIntegerField(serializers.IntegerField):
    """Custom integer field that properly handles null and empty values."""
    
    def to_internal_value(self, data):
        if data is None or data == '' or data == 'null':
            return None
        return super().to_internal_value(data)


class EquipmentSaleSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentSale objects."""
    milestone_structure = PaymentMilestoneStructureSerializer(read_only=True)
    milestone_structure_id = NullableIntegerField(write_only=True, required=False, allow_null=True)
    unit_price = serializers.ReadOnlyField()
    can_assign_milestone = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentSale
        fields = [
            'id', 'name', 'vendor', 'sale_type', 'quantity', 'total_amount', 
            'milestone_structure', 'milestone_structure_id', 'project',
            'project_start_date', 'unit_price', 'can_assign_milestone', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_can_assign_milestone(self, obj):
        """Check if a milestone structure can be assigned to this sale."""
        return obj.can_assign_milestone_structure()


class EquipmentSaleScheduleSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentSale with milestone schedule data."""
    milestone_structure = PaymentMilestoneStructureSerializer(read_only=True)
    unit_price = serializers.ReadOnlyField()
    milestone_schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentSale
        fields = [
            'id', 'name', 'vendor', 'sale_type', 'quantity', 'total_amount',
            'milestone_structure', 'project', 'project_start_date', 'unit_price',
            'milestone_schedule', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_milestone_schedule(self, obj):
        """Get the milestone schedule data for gantt chart."""
        return obj.get_milestone_schedule()


class MilestoneAssignmentSerializer(serializers.Serializer):
    """Serializer for assigning milestone structures to equipment sales."""
    milestone_structure_id = serializers.IntegerField()
    
    def validate_milestone_structure_id(self, value):
        """Validate that the milestone structure exists."""
        from milestones.models import PaymentMilestoneStructure
        try:
            PaymentMilestoneStructure.objects.get(id=value)
        except PaymentMilestoneStructure.DoesNotExist:
            raise serializers.ValidationError("Milestone structure does not exist")
        return value
    
    def validate(self, attrs):
        """Validate that the sale can accept a milestone structure assignment."""
        sale = self.context['sale']
        if not sale.can_assign_milestone_structure():
            raise serializers.ValidationError("This sale already has a milestone structure assigned")
        return attrs