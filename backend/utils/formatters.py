"""
Formatting utilities for milestone and equipment operations.

This module contains data formatting and conversion functions
for consistent data presentation across the application.
"""

from decimal import Decimal
from datetime import datetime, date
from typing import Union, Dict, Any


def format_currency(amount: Union[Decimal, float, int], currency: str = "USD") -> str:
    """
    Format a numeric amount as currency.
    
    Args:
        amount: Amount to format
        currency: Currency code (default: USD)
    
    Returns:
        Formatted currency string
    """
    if currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def format_date_range(start_date: str, end_date: str) -> str:
    """
    Format a date range as a readable string.
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
    
    Returns:
        Formatted date range string
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').strftime('%b %d, %Y')
        end = datetime.strptime(end_date, '%Y-%m-%d').strftime('%b %d, %Y')
        return f"{start} - {end}"
    except ValueError:
        return f"{start_date} - {end_date}"


def format_percentage(value: Union[Decimal, float], decimal_places: int = 2) -> str:
    """
    Format a decimal value as a percentage.
    
    Args:
        value: Value to format (e.g., 0.15 for 15%)
        decimal_places: Number of decimal places to show
    
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimal_places}f}%"


def format_duration_days(days: int) -> str:
    """
    Format duration in days as a readable string.
    
    Args:
        days: Number of days
    
    Returns:
        Formatted duration string
    """
    if days == 0:
        return "Same day"
    elif days == 1:
        return "1 day"
    elif days < 7:
        return f"{days} days"
    elif days < 30:
        weeks = days // 7
        remaining_days = days % 7
        if remaining_days == 0:
            return f"{weeks} week{'s' if weeks > 1 else ''}"
        else:
            return f"{weeks} week{'s' if weeks > 1 else ''} {remaining_days} day{'s' if remaining_days > 1 else ''}"
    elif days < 365:
        months = days // 30
        remaining_days = days % 30
        if remaining_days == 0:
            return f"{months} month{'s' if months > 1 else ''}"
        else:
            return f"{months} month{'s' if months > 1 else ''} {remaining_days} day{'s' if remaining_days > 1 else ''}"
    else:
        years = days // 365
        remaining_days = days % 365
        if remaining_days == 0:
            return f"{years} year{'s' if years > 1 else ''}"
        else:
            return f"{years} year{'s' if years > 1 else ''} {remaining_days} day{'s' if remaining_days > 1 else ''}"


def format_milestone_summary(milestone_data: Dict[str, Any]) -> str:
    """
    Format milestone data as a summary string.
    
    Args:
        milestone_data: Dictionary containing milestone information
    
    Returns:
        Formatted milestone summary
    """
    name = milestone_data.get('name', 'Unnamed Milestone')
    percentage = milestone_data.get('payment_percentage', 0)
    amount = milestone_data.get('payment_amount', 0)
    due_date = milestone_data.get('due_date', '')
    
    try:
        formatted_date = datetime.strptime(due_date, '%Y-%m-%d').strftime('%b %d, %Y')
    except (ValueError, TypeError):
        formatted_date = due_date
    
    return f"{name}: {format_percentage(percentage/100)} (${amount:,.2f}) due {formatted_date}"


def format_equipment_summary(equipment_data: Dict[str, Any]) -> str:
    """
    Format equipment sale data as a summary string.
    
    Args:
        equipment_data: Dictionary containing equipment information
    
    Returns:
        Formatted equipment summary
    """
    name = equipment_data.get('name', 'Unnamed Equipment')
    quantity = equipment_data.get('quantity', 0)
    total_amount = equipment_data.get('total_amount', 0)
    unit_price = total_amount / quantity if quantity > 0 else 0
    
    return f"{name}: {quantity} units @ {format_currency(unit_price)} each = {format_currency(total_amount)}"


def format_phone_number(phone: str) -> str:
    """
    Format a phone number string.
    
    Args:
        phone: Raw phone number string
    
    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes as a readable string.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"
