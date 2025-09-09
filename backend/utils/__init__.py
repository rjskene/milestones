"""
Utils package for milestone backend.

This package contains reusable logic functions that can be imported
and used across different parts of the application.

Modules:
- calculations: Mathematical and financial calculations
- validators: Data validation functions
- formatters: Data formatting and conversion functions
- helpers: General utility functions
"""

# Import commonly used functions for easy access
from .calculations import calculate_payment_schedule, calculate_unit_price
from .validators import validate_payment_percentages, validate_milestone_dates
from .formatters import format_currency, format_date_range

__all__ = [
    'calculate_payment_schedule',
    'calculate_unit_price', 
    'validate_payment_percentages',
    'validate_milestone_dates',
    'format_currency',
    'format_date_range',
]
