from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PaymentMilestoneStructure(models.Model):
    """
    A reusable payment milestone structure with a unique name.
    Contains multiple PaymentMilestone objects that define the payment schedule.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Unique name for this milestone structure")
    description = models.TextField(blank=True, help_text="Optional description of this milestone structure")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PaymentMilestone(models.Model):
    """
    Individual milestone within a PaymentMilestoneStructure.
    Defines payment percentage, net terms, and timing.
    """
    structure = models.ForeignKey(
        PaymentMilestoneStructure, 
        on_delete=models.CASCADE, 
        related_name='milestones'
    )
    name = models.CharField(max_length=100, help_text="Name of this milestone (e.g., 'Down Payment', 'Final Payment')")
    payment_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of total payment due (0-100)"
    )
    net_terms_days = models.PositiveIntegerField(
        default=0,
        help_text="Number of days after milestone due date for payment terms"
    )
    days_after_previous = models.PositiveIntegerField(
        default=0,
        help_text="Days after previous milestone (0 for first milestone)"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of this milestone within the structure"
    )

    class Meta:
        ordering = ['structure', 'order']
        unique_together = ['structure', 'order']

    def __str__(self):
        return f"{self.structure.name} - {self.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Ensure payment percentages don't exceed 100% total
        if self.structure_id:
            total_percentage = sum(
                milestone.payment_percentage 
                for milestone in self.structure.milestones.exclude(id=self.id)
            ) + self.payment_percentage
            
            if total_percentage > 100:
                raise ValidationError(
                    f"Total payment percentage cannot exceed 100%. "
                    f"Current total would be {total_percentage}%"
                )