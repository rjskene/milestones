from rest_framework import serializers
from .models import PaymentMilestoneStructure, PaymentMilestone


class PaymentMilestoneSerializer(serializers.ModelSerializer):
    """Serializer for individual PaymentMilestone objects."""
    
    class Meta:
        model = PaymentMilestone
        fields = ['id', 'name', 'payment_percentage', 'net_terms_days', 'days_after_previous', 'order']


class PaymentMilestoneStructureSerializer(serializers.ModelSerializer):
    """Serializer for PaymentMilestoneStructure with nested milestones."""
    milestones = PaymentMilestoneSerializer(many=True, read_only=True)
    
    class Meta:
        model = PaymentMilestoneStructure
        fields = ['id', 'name', 'description', 'milestones', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PaymentMilestoneStructureCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating PaymentMilestoneStructure with milestones."""
    milestones = PaymentMilestoneSerializer(many=True)
    
    class Meta:
        model = PaymentMilestoneStructure
        fields = ['name', 'description', 'milestones']
    
    def create(self, validated_data):
        milestones_data = validated_data.pop('milestones')
        structure = PaymentMilestoneStructure.objects.create(**validated_data)
        
        for milestone_data in milestones_data:
            PaymentMilestone.objects.create(structure=structure, **milestone_data)
        
        return structure
    
    def update(self, instance, validated_data):
        milestones_data = validated_data.pop('milestones', None)
        
        # Update structure fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update milestones if provided
        if milestones_data is not None:
            # Delete existing milestones
            instance.milestones.all().delete()
            
            # Create new milestones
            for milestone_data in milestones_data:
                PaymentMilestone.objects.create(structure=instance, **milestone_data)
        
        return instance


