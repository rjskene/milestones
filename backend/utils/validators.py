"""
Validation utilities for milestone and equipment operations.

This module contains data validation functions that can be used
to validate input data before processing.
"""

from decimal import Decimal
from typing import List, Dict, Any, Tuple
from datetime import datetime


def validate_payment_percentages(milestones: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    Validate that payment percentages don't exceed 100% total.
    
    Args:
        milestones: List of milestone dictionaries with payment_percentage
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    total_percentage = sum(milestone.get('payment_percentage', 0) for milestone in milestones)
    
    if total_percentage > 100:
        return False, f"Total payment percentage cannot exceed 100%. Current total: {total_percentage}%"
    
    if total_percentage < 0:
        return False, f"Total payment percentage cannot be negative. Current total: {total_percentage}%"
    
    return True, ""


def validate_milestone_dates(
    project_start_date: str,
    milestones: List[Dict[str, Any]]
) -> Tuple[bool, str]:
    """
    Validate milestone date calculations.
    
    Args:
        project_start_date: Start date in ISO format (YYYY-MM-DD)
        milestones: List of milestone dictionaries with days_after_previous
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        start_date = datetime.strptime(project_start_date, '%Y-%m-%d').date()
    except ValueError:
        return False, "Invalid project start date format. Use YYYY-MM-DD"
    
    cumulative_days = 0
    
    for i, milestone in enumerate(milestones):
        days_after_previous = milestone.get('days_after_previous', 0)
        
        if days_after_previous < 0:
            return False, f"Milestone {i+1}: days_after_previous cannot be negative"
        
        cumulative_days += days_after_previous
        
        # Check if milestone date is too far in the future (optional business rule)
        if cumulative_days > 3650:  # 10 years
            return False, f"Milestone {i+1}: Date is more than 10 years from project start"
    
    return True, ""


def validate_equipment_sale_data(
    name: str,
    quantity: int,
    total_amount: Decimal,
    vendor: str = ""
) -> Tuple[bool, str]:
    """
    Validate equipment sale data.
    
    Args:
        name: Equipment name
        quantity: Number of units
        total_amount: Total sale amount
        vendor: Vendor name (optional)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Equipment name is required"
    
    if quantity <= 0:
        return False, "Quantity must be greater than 0"
    
    if total_amount <= 0:
        return False, "Total amount must be greater than 0"
    
    if len(name) > 200:
        return False, "Equipment name cannot exceed 200 characters"
    
    if vendor and len(vendor) > 200:
        return False, "Vendor name cannot exceed 200 characters"
    
    return True, ""


def validate_decimal_range(
    value: Decimal,
    min_value: Decimal = None,
    max_value: Decimal = None,
    field_name: str = "Value"
) -> Tuple[bool, str]:
    """
    Validate that a decimal value is within a specified range.
    
    Args:
        value: Decimal value to validate
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if min_value is not None and value < min_value:
        return False, f"{field_name} must be at least {min_value}"
    
    if max_value is not None and value > max_value:
        return False, f"{field_name} must be at most {max_value}"
    
    return True, ""


def validate_date_format(date_string: str, field_name: str = "Date") -> Tuple[bool, str]:
    """
    Validate date string format.
    
    Args:
        date_string: Date string to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True, ""
    except ValueError:
        return False, f"{field_name} must be in YYYY-MM-DD format"


def validate_positive_integer(value: int, field_name: str = "Value") -> Tuple[bool, str]:
    """
    Validate that an integer is positive.
    
    Args:
        value: Integer value to validate
        field_name: Name of the field for error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, int):
        return False, f"{field_name} must be an integer"
    
    if value <= 0:
        return False, f"{field_name} must be positive"
    
    return True, ""
