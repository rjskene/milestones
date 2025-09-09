"""
Helper utilities for milestone and equipment operations.

This module contains general utility functions that can be used
across different parts of the application.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Union
import json


def get_current_date_string() -> str:
    """
    Get current date as ISO format string.
    
    Returns:
        Current date in YYYY-MM-DD format
    """
    return date.today().isoformat()


def get_current_datetime_string() -> str:
    """
    Get current datetime as ISO format string.
    
    Returns:
        Current datetime in YYYY-MM-DDTHH:MM:SS format
    """
    return datetime.now().isoformat()


def add_days_to_date(date_string: str, days: int) -> str:
    """
    Add days to a date string.
    
    Args:
        date_string: Date in ISO format (YYYY-MM-DD)
        days: Number of days to add (can be negative)
    
    Returns:
        New date in ISO format (YYYY-MM-DD)
    """
    try:
        original_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        new_date = original_date + timedelta(days=days)
        return new_date.isoformat()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}. Use YYYY-MM-DD")


def get_date_range(start_date: str, end_date: str) -> List[str]:
    """
    Get list of dates between start and end date (inclusive).
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
    
    Returns:
        List of date strings in ISO format
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        dates = []
        current = start
        while current <= end:
            dates.append(current.isoformat())
            current += timedelta(days=1)
        
        return dates
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")


def safe_json_loads(json_string: str, default: Any = None) -> Any:
    """
    Safely parse JSON string with fallback to default value.
    
    Args:
        json_string: JSON string to parse
        default: Default value if parsing fails
    
    Returns:
        Parsed JSON object or default value
    """
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """
    Safely serialize object to JSON string with fallback.
    
    Args:
        obj: Object to serialize
        default: Default JSON string if serialization fails
    
    Returns:
        JSON string or default value
    """
    try:
        return json.dumps(obj, default=str)
    except (TypeError, ValueError):
        return default


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")
    
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_duplicates_preserve_order(lst: List[Any]) -> List[Any]:
    """
    Remove duplicates from list while preserving order.
    
    Args:
        lst: List to deduplicate
    
    Returns:
        List with duplicates removed
    """
    seen = set()
    result = []
    
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result


def get_nested_value(data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get value from nested dictionary using dot notation.
    
    Args:
        data: Dictionary to search
        key_path: Dot-separated key path (e.g., "user.profile.name")
        default: Default value if key not found
    
    Returns:
        Value at key path or default
    """
    keys = key_path.split('.')
    current = data
    
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default


def set_nested_value(data: Dict[str, Any], key_path: str, value: Any) -> None:
    """
    Set value in nested dictionary using dot notation.
    
    Args:
        data: Dictionary to modify
        key_path: Dot-separated key path (e.g., "user.profile.name")
        value: Value to set
    """
    keys = key_path.split('.')
    current = data
    
    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # Set the final value
    current[keys[-1]] = value


def merge_dictionaries(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries, with dict2 values taking precedence.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result


def is_weekend(date_string: str) -> bool:
    """
    Check if a date falls on a weekend.
    
    Args:
        date_string: Date in ISO format (YYYY-MM-DD)
    
    Returns:
        True if date is weekend, False otherwise
    """
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
        return date_obj.weekday() >= 5  # Saturday = 5, Sunday = 6
    except ValueError:
        return False


def get_business_days_between(start_date: str, end_date: str) -> int:
    """
    Calculate number of business days between two dates.
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
    
    Returns:
        Number of business days
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        business_days = 0
        current = start
        
        while current <= end:
            if current.weekday() < 5:  # Monday = 0, Friday = 4
                business_days += 1
            current += timedelta(days=1)
        
        return business_days
    except ValueError:
        return 0
