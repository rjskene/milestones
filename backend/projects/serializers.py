from rest_framework import serializers
from .models import Project
from equipment.serializers import EquipmentSaleSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project objects."""
    equipment_sales = EquipmentSaleSerializer(many=True, read_only=True)
    total_value = serializers.ReadOnlyField()
    equipment_sales_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'start_date', 'description', 
            'equipment_sales', 'total_value', 'equipment_sales_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProjectTimelineSerializer(serializers.ModelSerializer):
    """Serializer for Project with timeline data for gantt chart."""
    equipment_sales = EquipmentSaleSerializer(many=True, read_only=True)
    total_value = serializers.ReadOnlyField()
    equipment_sales_count = serializers.ReadOnlyField()
    project_timeline = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'start_date', 'description',
            'equipment_sales', 'total_value', 'equipment_sales_count',
            'project_timeline', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_project_timeline(self, obj):
        """Get the project timeline data for gantt chart."""
        return obj.get_project_timeline()
