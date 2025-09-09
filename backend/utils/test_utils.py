import unittest
from decimal import Decimal
from datetime import date, timedelta
from .calculations import calculate_payment_schedule, calculate_unit_price
from .validators import validate_payment_percentages, validate_milestone_data
from .formatters import format_currency, format_date


class CalculationsTest(unittest.TestCase):
    """Test cases for calculation utility functions."""
    
    def test_calculate_unit_price(self):
        """Test unit price calculation."""
        # Test normal case
        unit_price = calculate_unit_price(Decimal('1000.00'), 5)
        self.assertEqual(unit_price, Decimal('200.00'))
        
        # Test with zero quantity
        unit_price = calculate_unit_price(Decimal('1000.00'), 0)
        self.assertEqual(unit_price, Decimal('0.00'))
        
        # Test with one item
        unit_price = calculate_unit_price(Decimal('1000.00'), 1)
        self.assertEqual(unit_price, Decimal('1000.00'))
    
    def test_calculate_payment_schedule(self):
        """Test payment schedule calculation."""
        total_amount = Decimal('100000.00')
        milestones = [
            {
                'payment_percentage': Decimal('30.00'),
                'days_after_previous': 0,
                'net_terms_days': 0
            },
            {
                'payment_percentage': Decimal('70.00'),
                'days_after_previous': 30,
                'net_terms_days': 30
            }
        ]
        start_date = date(2024, 1, 1)
        
        schedule = calculate_payment_schedule(total_amount, milestones, start_date)
        
        self.assertEqual(len(schedule), 2)
        
        # Test first milestone
        first_milestone = schedule[0]
        self.assertEqual(first_milestone['payment_amount'], Decimal('30000.00'))
        self.assertEqual(first_milestone['start_days'], 0)
        self.assertEqual(first_milestone['end_days'], 0)
        self.assertEqual(first_milestone['due_date'], start_date)
        self.assertEqual(first_milestone['payment_due_date'], start_date)
        
        # Test second milestone
        second_milestone = schedule[1]
        self.assertEqual(second_milestone['payment_amount'], Decimal('70000.00'))
        self.assertEqual(second_milestone['start_days'], 0)
        self.assertEqual(second_milestone['end_days'], 30)
        self.assertEqual(second_milestone['due_date'], start_date + timedelta(days=30))
        self.assertEqual(second_milestone['payment_due_date'], start_date + timedelta(days=60))


class ValidatorsTest(unittest.TestCase):
    """Test cases for validation utility functions."""
    
    def test_validate_payment_percentages_valid(self):
        """Test valid payment percentages."""
        milestones = [
            {'payment_percentage': Decimal('30.00')},
            {'payment_percentage': Decimal('70.00')}
        ]
        
        is_valid, error = validate_payment_percentages(milestones)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_payment_percentages_exceeds_100(self):
        """Test payment percentages that exceed 100%."""
        milestones = [
            {'payment_percentage': Decimal('60.00')},
            {'payment_percentage': Decimal('60.00')}  # Total: 120%
        ]
        
        is_valid, error = validate_payment_percentages(milestones)
        self.assertFalse(is_valid)
        self.assertIn('Total payment percentage cannot exceed 100%', error)
    
    def test_validate_payment_percentages_negative(self):
        """Test negative payment percentages."""
        milestones = [
            {'payment_percentage': Decimal('-10.00')},
            {'payment_percentage': Decimal('110.00')}
        ]
        
        is_valid, error = validate_payment_percentages(milestones)
        self.assertFalse(is_valid)
        self.assertIn('Payment percentages must be between 0 and 100', error)
    
    def test_validate_milestone_data_valid(self):
        """Test valid milestone data."""
        milestone_data = {
            'name': 'Test Milestone',
            'payment_percentage': Decimal('50.00'),
            'days_after_previous': 30,
            'net_terms_days': 15
        }
        
        is_valid, error = validate_milestone_data(milestone_data)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_milestone_data_missing_name(self):
        """Test milestone data with missing name."""
        milestone_data = {
            'payment_percentage': Decimal('50.00'),
            'days_after_previous': 30,
            'net_terms_days': 15
        }
        
        is_valid, error = validate_milestone_data(milestone_data)
        self.assertFalse(is_valid)
        self.assertIn('Name is required', error)
    
    def test_validate_milestone_data_invalid_percentage(self):
        """Test milestone data with invalid percentage."""
        milestone_data = {
            'name': 'Test Milestone',
            'payment_percentage': Decimal('150.00'),
            'days_after_previous': 30,
            'net_terms_days': 15
        }
        
        is_valid, error = validate_milestone_data(milestone_data)
        self.assertFalse(is_valid)
        self.assertIn('Payment percentage must be between 0 and 100', error)


class FormattersTest(unittest.TestCase):
    """Test cases for formatting utility functions."""
    
    def test_format_currency(self):
        """Test currency formatting."""
        # Test normal case
        formatted = format_currency(Decimal('1234.56'))
        self.assertEqual(formatted, '$1,234.56')
        
        # Test zero
        formatted = format_currency(Decimal('0.00'))
        self.assertEqual(formatted, '$0.00')
        
        # Test large number
        formatted = format_currency(Decimal('1234567.89'))
        self.assertEqual(formatted, '$1,234,567.89')
        
        # Test negative number
        formatted = format_currency(Decimal('-1234.56'))
        self.assertEqual(formatted, '-$1,234.56')
    
    def test_format_date(self):
        """Test date formatting."""
        test_date = date(2024, 1, 15)
        
        # Test default format
        formatted = format_date(test_date)
        self.assertEqual(formatted, '2024-01-15')
        
        # Test custom format
        formatted = format_date(test_date, '%B %d, %Y')
        self.assertEqual(formatted, 'January 15, 2024')
        
        # Test with datetime
        from datetime import datetime
        test_datetime = datetime(2024, 1, 15, 14, 30, 0)
        formatted = format_date(test_datetime)
        self.assertEqual(formatted, '2024-01-15')


if __name__ == '__main__':
    unittest.main()
