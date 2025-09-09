"""
Examples of how to use the utils package in Django views and other parts of the application.

This file demonstrates various ways to import and use the utility functions.
"""

from decimal import Decimal
from django.http import JsonResponse
from django.views import View

# Import from the utils package
from utils.calculations import (
    calculate_payment_schedule,
    calculate_unit_price,
    calculate_total_payment_percentage
)
from utils.validators import (
    validate_payment_percentages,
    validate_equipment_sale_data,
    validate_date_format
)
from utils.formatters import (
    format_currency,
    format_percentage,
    format_milestone_summary
)
from utils.helpers import (
    get_current_date_string,
    add_days_to_date,
    get_business_days_between
)


class ExampleUsageInView(View):
    """
    Example Django view showing how to use utility functions.
    """
    
    def post(self, request):
        """Example POST endpoint using utility functions."""
        
        # Example: Validate equipment sale data
        equipment_data = {
            'name': request.POST.get('name', ''),
            'quantity': int(request.POST.get('quantity', 0)),
            'total_amount': Decimal(request.POST.get('total_amount', 0)),
            'vendor': request.POST.get('vendor', '')
        }
        
        is_valid, error_message = validate_equipment_sale_data(**equipment_data)
        if not is_valid:
            return JsonResponse({'error': error_message}, status=400)
        
        # Example: Calculate unit price
        unit_price = calculate_unit_price(
            equipment_data['total_amount'],
            equipment_data['quantity']
        )
        
        # Example: Format currency
        formatted_total = format_currency(equipment_data['total_amount'])
        formatted_unit_price = format_currency(unit_price)
        
        return JsonResponse({
            'equipment_name': equipment_data['name'],
            'total_amount': formatted_total,
            'unit_price': formatted_unit_price,
            'quantity': equipment_data['quantity']
        })


def example_calculation_function():
    """
    Example standalone function using utility functions.
    """
    
    # Example milestone data
    milestones = [
        {
            'name': 'Down Payment',
            'payment_percentage': 30,
            'days_after_previous': 0,
            'net_terms_days': 0
        },
        {
            'name': 'Progress Payment',
            'payment_percentage': 50,
            'days_after_previous': 30,
            'net_terms_days': 15
        },
        {
            'name': 'Final Payment',
            'payment_percentage': 20,
            'days_after_previous': 60,
            'net_terms_days': 30
        }
    ]
    
    # Validate payment percentages
    is_valid, error = validate_payment_percentages(milestones)
    if not is_valid:
        print(f"Validation error: {error}")
        return
    
    # Calculate payment schedule
    total_amount = Decimal('100000.00')
    project_start = get_current_date_string()
    
    schedule = calculate_payment_schedule(total_amount, milestones, project_start)
    
    # Format and display results
    print("Payment Schedule:")
    for milestone in schedule:
        summary = format_milestone_summary(milestone)
        print(f"  {summary}")
    
    # Calculate total percentage
    total_percentage = calculate_total_payment_percentage(milestones)
    print(f"\nTotal Payment Percentage: {format_percentage(total_percentage/100)}")
    
    return schedule


def example_date_calculations():
    """
    Example of date-related utility functions.
    """
    
    # Get current date
    today = get_current_date_string()
    print(f"Today: {today}")
    
    # Add days to date
    future_date = add_days_to_date(today, 30)
    print(f"30 days from today: {future_date}")
    
    # Calculate business days
    business_days = get_business_days_between(today, future_date)
    print(f"Business days between: {business_days}")


def example_validation_workflow():
    """
    Example of a complete validation workflow.
    """
    
    # Example data to validate
    equipment_data = {
        'name': 'Industrial Mixer',
        'quantity': 5,
        'total_amount': Decimal('50000.00'),
        'vendor': 'ABC Equipment Co.'
    }
    
    milestones = [
        {'payment_percentage': 25, 'days_after_previous': 0, 'net_terms_days': 0},
        {'payment_percentage': 50, 'days_after_previous': 30, 'net_terms_days': 15},
        {'payment_percentage': 25, 'days_after_previous': 60, 'net_terms_days': 30}
    ]
    
    project_start = '2024-01-01'
    
    # Validate equipment data
    is_valid, error = validate_equipment_sale_data(**equipment_data)
    if not is_valid:
        print(f"Equipment validation failed: {error}")
        return False
    
    # Validate payment percentages
    is_valid, error = validate_payment_percentages(milestones)
    if not is_valid:
        print(f"Payment validation failed: {error}")
        return False
    
    # Validate date format
    is_valid, error = validate_date_format(project_start, "Project Start Date")
    if not is_valid:
        print(f"Date validation failed: {error}")
        return False
    
    print("All validations passed!")
    return True


# Example of using utilities in a Django model method
class ExampleModelUsage:
    """
    Example showing how to use utilities in Django model methods.
    """
    
    def __init__(self, name, total_amount, quantity):
        self.name = name
        self.total_amount = total_amount
        self.quantity = quantity
    
    def get_formatted_summary(self):
        """Example method using utility functions."""
        from utils.formatters import format_currency, format_equipment_summary
        
        unit_price = calculate_unit_price(self.total_amount, self.quantity)
        
        return {
            'name': self.name,
            'total_formatted': format_currency(self.total_amount),
            'unit_price_formatted': format_currency(unit_price),
            'summary': format_equipment_summary({
                'name': self.name,
                'quantity': self.quantity,
                'total_amount': self.total_amount
            })
        }


if __name__ == "__main__":
    # Run examples when script is executed directly
    print("=== Example Calculation Function ===")
    example_calculation_function()
    
    print("\n=== Example Date Calculations ===")
    example_date_calculations()
    
    print("\n=== Example Validation Workflow ===")
    example_validation_workflow()
    
    print("\n=== Example Model Usage ===")
    example_model = ExampleModelUsage("Test Equipment", Decimal('25000.00'), 3)
    summary = example_model.get_formatted_summary()
    print(f"Model Summary: {summary}")
