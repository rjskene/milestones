from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta
from milestones.models import PaymentMilestoneStructure


class EquipmentSale(models.Model):
    """
    Equipment sale that uses a PaymentMilestoneStructure to define payment schedule.
    Can be associated with a Project or standalone.
    """
    SALE_TYPE_CHOICES = [
        ('vendor', 'Vendor Sale'),
        ('customer', 'Customer Sale'),
    ]
    
    name = models.CharField(max_length=200, help_text="Name of the equipment sale")
    vendor = models.CharField(max_length=200, blank=True, help_text="Vendor name (optional)")
    sale_type = models.CharField(
        max_length=10,
        choices=SALE_TYPE_CHOICES,
        default='vendor',
        help_text="Type of sale - Vendor or Customer"
    )
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
        null=True,
        blank=True,
        help_text="Payment milestone structure to use for this sale (can be assigned later)"
    )
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='equipment_sales',
        help_text="Project this sale belongs to (optional)"
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
        Returns empty list if no milestone structure is assigned.
        """
        if not self.milestone_structure:
            return []
            
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
    
    def can_assign_milestone_structure(self):
        """
        Check if a milestone structure can be assigned to this sale.
        Returns True if no milestone structure is currently assigned.
        """
        return self.milestone_structure is None
    
    def assign_milestone_structure(self, milestone_structure):
        """
        Assign a milestone structure to this sale.
        Raises ValueError if a milestone structure is already assigned.
        """
        if not self.can_assign_milestone_structure():
            raise ValueError("A milestone structure is already assigned to this sale")
        
        self.milestone_structure = milestone_structure
        self.save()