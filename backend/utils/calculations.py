"""
Calculation utilities for milestone and equipment operations.

This module contains mathematical and financial calculation functions
that can be used across the application.
"""

from decimal import Decimal
from datetime import timedelta
from typing import List, Dict, Any


def calculate_payment_schedule(
    total_amount: Decimal,
    milestones: List[Dict[str, Any]],
    project_start_date: str
) -> List[Dict[str, Any]]:
    """
    Calculate payment schedule based on milestone structure.
    
    Args:
        total_amount: Total amount for the project
        milestones: List of milestone dictionaries with payment_percentage, 
                   days_after_previous, net_terms_days
        project_start_date: Start date in ISO format (YYYY-MM-DD)
    
    Returns:
        List of dictionaries with calculated payment information
    """
    from datetime import datetime
    
    schedule = []
    cumulative_days = 0
    start_date = datetime.strptime(project_start_date, '%Y-%m-%d').date()
    
    for milestone in milestones:
        # Calculate start and end dates
        start_days = cumulative_days
        end_days = cumulative_days + milestone.get('days_after_previous', 0)
        
        # Calculate payment amounts
        payment_percentage = Decimal(str(milestone.get('payment_percentage', 0)))
        payment_amount = (total_amount * payment_percentage) / 100
        
        # Calculate dates
        due_date = start_date + timedelta(days=end_days)
        net_terms_days = milestone.get('net_terms_days', 0)
        payment_due_date = due_date + timedelta(days=net_terms_days)
        
        schedule.append({
            'name': milestone.get('name', ''),
            'start_days': start_days,
            'end_days': end_days,
            'payment_percentage': float(payment_percentage),
            'payment_amount': float(payment_amount),
            'due_date': due_date.isoformat(),
            'payment_due_date': payment_due_date.isoformat(),
            'net_terms_days': net_terms_days,
        })
        
        cumulative_days = end_days
    
    return schedule


def calculate_unit_price(total_amount: Decimal, quantity: int) -> Decimal:
    """
    Calculate unit price based on total amount and quantity.
    
    Args:
        total_amount: Total amount for the sale
        quantity: Number of units
    
    Returns:
        Unit price as Decimal
    """
    if quantity <= 0:
        return Decimal('0')
    return total_amount / quantity


def calculate_total_payment_percentage(milestones: List[Dict[str, Any]]) -> float:
    """
    Calculate total payment percentage from milestone list.
    
    Args:
        milestones: List of milestone dictionaries with payment_percentage
    
    Returns:
        Total percentage as float
    """
    return sum(milestone.get('payment_percentage', 0) for milestone in milestones)


def calculate_days_between_dates(start_date: str, end_date: str) -> int:
    """
    Calculate number of days between two dates.
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
    
    Returns:
        Number of days between dates
    """
    from datetime import datetime
    
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    return (end - start).days


def calculate_compound_interest(
    principal: Decimal,
    rate: Decimal,
    time_periods: int,
    compounding_frequency: int = 1
) -> Decimal:
    """
    Calculate compound interest.
    
    Args:
        principal: Initial amount
        rate: Interest rate (as decimal, e.g., 0.05 for 5%)
        time_periods: Number of time periods
        compounding_frequency: How many times per period interest is compounded
    
    Returns:
        Final amount after compound interest
    """
    return principal * (1 + rate / compounding_frequency) ** (compounding_frequency * time_periods)
