from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta
from milestones.models import PaymentMilestoneStructure


class EquipmentSale(models.Model):
    """
    Equipment sale that uses a PaymentMilestoneStructure to define payment schedule.
    """
    name = models.CharField(max_length=200, help_text="Name of the equipment sale")
    vendor = models.CharField(max_length=200, blank=True, help_text="Vendor name (optional)")
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity of equipment to be sold"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Total dollar amount for the sale"
    )
    milestone_structure = models.ForeignKey(
        PaymentMilestoneStructure,
        on_delete=models.CASCADE,
        help_text="Payment milestone structure to use for this sale"
    )
    project_start_date = models.DateField(
        help_text="Date when the project commences (day 0 for milestone calculations)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - ${self.total_amount}"

    @property
    def unit_price(self):
        """Calculate unit price based on total amount and quantity."""
        return self.total_amount / self.quantity if self.quantity > 0 else 0

    def get_milestone_schedule(self):
        """
        Generate milestone schedule data for gantt chart.
        Returns a list of dictionaries with milestone information.
        """
        milestones = self.milestone_structure.milestones.all().order_by('order')
        schedule = []
        cumulative_days = 0
        
        for milestone in milestones:
            # Calculate start and end dates
            start_days = cumulative_days
            end_days = cumulative_days + milestone.days_after_previous
            
            # Calculate payment amounts
            payment_amount = (self.total_amount * milestone.payment_percentage) / 100
            due_date = self.project_start_date + timedelta(days=end_days)
            payment_due_date = due_date + timedelta(days=milestone.net_terms_days)
            
            schedule.append({
                'id': milestone.id,
                'name': milestone.name,
                'start_days': start_days,
                'end_days': end_days,
                'payment_percentage': float(milestone.payment_percentage),
                'payment_amount': float(payment_amount),
                'due_date': due_date.isoformat(),
                'payment_due_date': payment_due_date.isoformat(),
                'net_terms_days': milestone.net_terms_days,
            })
            
            cumulative_days = end_days
        
        return schedule