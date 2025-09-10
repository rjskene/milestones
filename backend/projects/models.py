from django.db import models
from django.core.validators import MinValueValidator


class Project(models.Model):
    """
    Top-level project that contains multiple equipment sales.
    Each project has a name, start date, and collection of equipment sales.
    """
    SALE_TYPE_CHOICES = [
        ('vendor', 'Vendor Sale'),
        ('customer', 'Customer Sale'),
    ]
    
    name = models.CharField(max_length=200, help_text="Name of the project")
    start_date = models.DateField(help_text="Project start date")
    description = models.TextField(blank=True, help_text="Optional project description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def total_value(self):
        """Calculate total value of all equipment sales in this project."""
        return sum(sale.total_amount for sale in self.equipment_sales.all())

    @property
    def equipment_sales_count(self):
        """Get count of equipment sales in this project."""
        return self.equipment_sales.count()

    def get_project_timeline(self):
        """
        Generate timeline data for the entire project including all equipment sales.
        Returns data formatted for gantt chart visualization.
        """
        timeline_data = []
        
        for sale in self.equipment_sales.all():
            sale_schedule = sale.get_milestone_schedule()
            for milestone in sale_schedule:
                timeline_data.append({
                    'sale_id': sale.id,
                    'sale_name': sale.name,
                    'milestone_id': milestone['id'],
                    'milestone_name': milestone['name'],
                    'start_days': milestone['start_days'],
                    'end_days': milestone['end_days'],
                    'payment_percentage': milestone['payment_percentage'],
                    'payment_amount': milestone['payment_amount'],
                    'due_date': milestone['due_date'],
                    'payment_due_date': milestone['payment_due_date'],
                    'net_terms_days': milestone['net_terms_days'],
                })
        
        return timeline_data
