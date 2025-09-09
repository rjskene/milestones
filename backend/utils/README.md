# Utils Package

This package contains reusable logic functions for the milestone backend application. It's designed to be a lightweight, pure Python package that can be imported and used across different parts of the Django application.

## Structure

```
utils/
├── __init__.py          # Package initialization and common imports
├── calculations.py      # Mathematical and financial calculations
├── validators.py        # Data validation functions
├── formatters.py        # Data formatting and conversion functions
├── helpers.py          # General utility functions
├── examples.py         # Usage examples and demonstrations
└── README.md           # This documentation
```

## Quick Start

### Importing Functions

```python
# Import specific functions
from utils.calculations import calculate_payment_schedule, calculate_unit_price
from utils.validators import validate_payment_percentages
from utils.formatters import format_currency

# Import from package root (recommended for common functions)
from utils import calculate_payment_schedule, validate_payment_percentages, format_currency
```

### Basic Usage

```python
from decimal import Decimal
from utils import calculate_payment_schedule, validate_payment_percentages, format_currency

# Validate milestone data
milestones = [
    {'payment_percentage': 30, 'days_after_previous': 0, 'net_terms_days': 0},
    {'payment_percentage': 50, 'days_after_previous': 30, 'net_terms_days': 15},
    {'payment_percentage': 20, 'days_after_previous': 60, 'net_terms_days': 30}
]

is_valid, error = validate_payment_percentages(milestones)
if is_valid:
    # Calculate payment schedule
    schedule = calculate_payment_schedule(
        total_amount=Decimal('100000.00'),
        milestones=milestones,
        project_start_date='2024-01-01'
    )
    
    # Format results
    for milestone in schedule:
        print(f"{milestone['name']}: {format_currency(milestone['payment_amount'])}")
```

## Modules

### calculations.py

Mathematical and financial calculation functions.

**Key Functions:**
- `calculate_payment_schedule()` - Generate payment schedule from milestone structure
- `calculate_unit_price()` - Calculate unit price from total amount and quantity
- `calculate_total_payment_percentage()` - Sum payment percentages from milestone list
- `calculate_compound_interest()` - Calculate compound interest

**Example:**
```python
from utils.calculations import calculate_payment_schedule

schedule = calculate_payment_schedule(
    total_amount=Decimal('50000.00'),
    milestones=[
        {'payment_percentage': 50, 'days_after_previous': 0, 'net_terms_days': 0},
        {'payment_percentage': 50, 'days_after_previous': 30, 'net_terms_days': 15}
    ],
    project_start_date='2024-01-01'
)
```

### validators.py

Data validation functions for input validation.

**Key Functions:**
- `validate_payment_percentages()` - Ensure percentages don't exceed 100%
- `validate_equipment_sale_data()` - Validate equipment sale information
- `validate_date_format()` - Validate date string format
- `validate_decimal_range()` - Validate decimal values within range

**Example:**
```python
from utils.validators import validate_equipment_sale_data

is_valid, error = validate_equipment_sale_data(
    name="Industrial Mixer",
    quantity=5,
    total_amount=Decimal('50000.00'),
    vendor="ABC Equipment Co."
)

if not is_valid:
    print(f"Validation error: {error}")
```

### formatters.py

Data formatting and conversion functions for consistent presentation.

**Key Functions:**
- `format_currency()` - Format numbers as currency
- `format_percentage()` - Format decimals as percentages
- `format_date_range()` - Format date ranges as readable strings
- `format_milestone_summary()` - Format milestone data as summary

**Example:**
```python
from utils.formatters import format_currency, format_percentage

amount = Decimal('1234.56')
percentage = 0.15

print(format_currency(amount))      # $1,234.56
print(format_percentage(percentage)) # 15.00%
```

### helpers.py

General utility functions for common operations.

**Key Functions:**
- `get_current_date_string()` - Get current date as ISO string
- `add_days_to_date()` - Add days to a date string
- `get_business_days_between()` - Calculate business days between dates
- `safe_json_loads()` - Safely parse JSON with fallback
- `chunk_list()` - Split list into chunks

**Example:**
```python
from utils.helpers import get_current_date_string, add_days_to_date

today = get_current_date_string()           # '2024-01-15'
future = add_days_to_date(today, 30)        # '2024-02-14'
```

## Usage in Django

### In Views

```python
from django.http import JsonResponse
from django.views import View
from utils import validate_equipment_sale_data, calculate_unit_price, format_currency

class EquipmentView(View):
    def post(self, request):
        # Validate input
        is_valid, error = validate_equipment_sale_data(
            name=request.POST.get('name'),
            quantity=int(request.POST.get('quantity', 0)),
            total_amount=Decimal(request.POST.get('total_amount', 0))
        )
        
        if not is_valid:
            return JsonResponse({'error': error}, status=400)
        
        # Calculate and format
        unit_price = calculate_unit_price(total_amount, quantity)
        
        return JsonResponse({
            'unit_price': format_currency(unit_price)
        })
```

### In Models

```python
from django.db import models
from utils import calculate_unit_price, format_currency

class EquipmentSale(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    @property
    def unit_price(self):
        return calculate_unit_price(self.total_amount, self.quantity)
    
    def get_formatted_summary(self):
        return f"{self.name}: {format_currency(self.total_amount)}"
```

### In Management Commands

```python
from django.core.management.base import BaseCommand
from utils import get_current_date_string, calculate_payment_schedule

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Use utility functions in management commands
        today = get_current_date_string()
        self.stdout.write(f"Processing data for {today}")
        
        # ... rest of command logic
```

## Testing

You can test utility functions independently of Django:

```python
# test_utils.py
from decimal import Decimal
from utils import calculate_unit_price, validate_payment_percentages

def test_calculate_unit_price():
    result = calculate_unit_price(Decimal('100.00'), 5)
    assert result == Decimal('20.00')

def test_validate_payment_percentages():
    milestones = [{'payment_percentage': 50}, {'payment_percentage': 50}]
    is_valid, error = validate_payment_percentages(milestones)
    assert is_valid == True
    assert error == ""
```

## Best Practices

1. **Import what you need**: Import specific functions rather than entire modules when possible
2. **Use type hints**: All functions include type hints for better IDE support
3. **Handle errors**: Always check return values from validation functions
4. **Keep functions pure**: Utility functions should not have side effects
5. **Test independently**: You can test utility functions without Django context

## Adding New Functions

When adding new utility functions:

1. Choose the appropriate module based on function purpose
2. Add type hints for all parameters and return values
3. Include docstrings with examples
4. Add the function to `__init__.py` if it's commonly used
5. Update this README with usage examples

## Examples

See `examples.py` for comprehensive usage examples including:
- Django view integration
- Model method usage
- Standalone function examples
- Complete validation workflows
