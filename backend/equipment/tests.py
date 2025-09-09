from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta
from milestones.models import PaymentMilestoneStructure, PaymentMilestone
from .models import EquipmentSale


class EquipmentSaleModelTest(TestCase):
    """Test cases for EquipmentSale model."""
    
    def setUp(self):
        """Set up test data."""
        # Create a milestone structure
        self.structure = PaymentMilestoneStructure.objects.create(
            name="Test Structure",
            description="A test milestone structure"
        )
        
        # Create milestones
        self.milestone1 = PaymentMilestone.objects.create(
            structure=self.structure,
            name="Down Payment",
            payment_percentage=Decimal('30.00'),
            net_terms_days=0,
            days_after_previous=0,
            order=0
        )
        
        self.milestone2 = PaymentMilestone.objects.create(
            structure=self.structure,
            name="Final Payment",
            payment_percentage=Decimal('70.00'),
            net_terms_days=30,
            days_after_previous=30,
            order=1
        )
        
        # Create equipment sale
        self.equipment_sale = EquipmentSale.objects.create(
            name="Test Equipment Sale",
            vendor="Test Vendor",
            quantity=5,
            total_amount=Decimal('100000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
    
    def test_str_representation(self):
        """Test string representation of EquipmentSale."""
        expected = "Test Equipment Sale - $100000.00"
        self.assertEqual(str(self.equipment_sale), expected)
    
    def test_ordering(self):
        """Test that equipment sales are ordered by creation date (newest first)."""
        # Create another sale
        sale2 = EquipmentSale.objects.create(
            name="Second Sale",
            quantity=1,
            total_amount=Decimal('50000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        
        sales = list(EquipmentSale.objects.all())
        self.assertEqual(sales[0], sale2)  # Newest first
        self.assertEqual(sales[1], self.equipment_sale)
    
    def test_unit_price_property(self):
        """Test unit price calculation."""
        expected_unit_price = Decimal('100000.00') / 5
        self.assertEqual(self.equipment_sale.unit_price, expected_unit_price)
    
    def test_unit_price_with_zero_quantity(self):
        """Test unit price calculation with zero quantity."""
        sale = EquipmentSale.objects.create(
            name="Zero Quantity Sale",
            quantity=0,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        self.assertEqual(sale.unit_price, 0)
    
    def test_quantity_validation(self):
        """Test quantity validation."""
        # Test negative quantity
        sale = EquipmentSale(
            name="Invalid Sale",
            quantity=-1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        with self.assertRaises(ValidationError):
            sale.full_clean()
        
        # Test zero quantity
        sale.quantity = 0
        with self.assertRaises(ValidationError):
            sale.full_clean()
    
    def test_total_amount_validation(self):
        """Test total amount validation."""
        # Test negative amount
        sale = EquipmentSale(
            name="Invalid Sale",
            quantity=1,
            total_amount=Decimal('-1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        with self.assertRaises(ValidationError):
            sale.full_clean()
    
    def test_get_milestone_schedule(self):
        """Test milestone schedule generation."""
        schedule = self.equipment_sale.get_milestone_schedule()
        
        self.assertEqual(len(schedule), 2)
        
        # Test first milestone
        first_milestone = schedule[0]
        self.assertEqual(first_milestone['name'], 'Down Payment')
        self.assertEqual(first_milestone['start_days'], 0)
        self.assertEqual(first_milestone['end_days'], 0)
        self.assertEqual(first_milestone['payment_percentage'], 30.0)
        self.assertEqual(first_milestone['payment_amount'], 30000.0)
        self.assertEqual(first_milestone['net_terms_days'], 0)
        
        # Test second milestone
        second_milestone = schedule[1]
        self.assertEqual(second_milestone['name'], 'Final Payment')
        self.assertEqual(second_milestone['start_days'], 0)
        self.assertEqual(second_milestone['end_days'], 30)
        self.assertEqual(second_milestone['payment_percentage'], 70.0)
        self.assertEqual(second_milestone['payment_amount'], 70000.0)
        self.assertEqual(second_milestone['net_terms_days'], 30)
    
    def test_get_milestone_schedule_dates(self):
        """Test that milestone schedule includes correct dates."""
        start_date = date(2024, 1, 1)
        sale = EquipmentSale.objects.create(
            name="Date Test Sale",
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=start_date
        )
        
        schedule = sale.get_milestone_schedule()
        
        # First milestone: due immediately, payment due immediately
        first_milestone = schedule[0]
        expected_due_date = start_date
        expected_payment_due_date = start_date
        self.assertEqual(first_milestone['due_date'], expected_due_date.isoformat())
        self.assertEqual(first_milestone['payment_due_date'], expected_payment_due_date.isoformat())
        
        # Second milestone: due after 30 days, payment due after 30 + 30 = 60 days
        second_milestone = schedule[1]
        expected_due_date = start_date + timedelta(days=30)
        expected_payment_due_date = start_date + timedelta(days=60)
        self.assertEqual(second_milestone['due_date'], expected_due_date.isoformat())
        self.assertEqual(second_milestone['payment_due_date'], expected_payment_due_date.isoformat())
    
    def test_get_milestone_schedule_empty_structure(self):
        """Test milestone schedule with empty milestone structure."""
        empty_structure = PaymentMilestoneStructure.objects.create(name="Empty Structure")
        sale = EquipmentSale.objects.create(
            name="Empty Structure Sale",
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=empty_structure,
            project_start_date=date.today()
        )
        
        schedule = sale.get_milestone_schedule()
        self.assertEqual(len(schedule), 0)
    
    def test_cascade_delete_milestone_structure(self):
        """Test that deleting a milestone structure affects equipment sales."""
        sale_id = self.equipment_sale.id
        self.structure.delete()
        
        # Equipment sale should still exist but milestone_structure should be None
        # (Actually, with CASCADE, the sale should be deleted)
        self.assertFalse(EquipmentSale.objects.filter(id=sale_id).exists())


class EquipmentSaleIntegrationTest(TestCase):
    """Integration tests for EquipmentSale with PaymentMilestoneStructure."""
    
    def test_equipment_sale_with_complex_milestone_structure(self):
        """Test equipment sale with a complex milestone structure."""
        # Create a complex milestone structure
        structure = PaymentMilestoneStructure.objects.create(
            name="Complex Structure",
            description="A complex milestone structure with multiple payments"
        )
        
        # Create multiple milestones
        milestones_data = [
            {'name': 'Down Payment', 'percentage': 20, 'days': 0, 'net_terms': 0},
            {'name': 'Progress Payment 1', 'percentage': 30, 'days': 30, 'net_terms': 15},
            {'name': 'Progress Payment 2', 'percentage': 30, 'days': 60, 'net_terms': 15},
            {'name': 'Final Payment', 'percentage': 20, 'days': 90, 'net_terms': 30},
        ]
        
        for i, data in enumerate(milestones_data):
            PaymentMilestone.objects.create(
                structure=structure,
                name=data['name'],
                payment_percentage=Decimal(str(data['percentage'])),
                net_terms_days=data['net_terms'],
                days_after_previous=data['days'],
                order=i
            )
        
        # Create equipment sale
        sale = EquipmentSale.objects.create(
            name="Complex Equipment Sale",
            vendor="Complex Vendor",
            quantity=10,
            total_amount=Decimal('500000.00'),
            milestone_structure=structure,
            project_start_date=date(2024, 1, 1)
        )
        
        # Test milestone schedule
        schedule = sale.get_milestone_schedule()
        self.assertEqual(len(schedule), 4)
        
        # Verify payment amounts
        expected_amounts = [100000, 150000, 150000, 100000]  # 20%, 30%, 30%, 20%
        for i, milestone in enumerate(schedule):
            self.assertEqual(milestone['payment_amount'], expected_amounts[i])
        
        # Verify cumulative days
        expected_end_days = [0, 30, 60, 90]
        for i, milestone in enumerate(schedule):
            self.assertEqual(milestone['end_days'], expected_end_days[i])
    
    def test_multiple_equipment_sales_same_structure(self):
        """Test multiple equipment sales using the same milestone structure."""
        structure = PaymentMilestoneStructure.objects.create(name="Shared Structure")
        
        PaymentMilestone.objects.create(
            structure=structure,
            name="Payment",
            payment_percentage=Decimal('100.00'),
            order=0
        )
        
        # Create multiple sales with the same structure
        sale1 = EquipmentSale.objects.create(
            name="Sale 1",
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=structure,
            project_start_date=date.today()
        )
        
        sale2 = EquipmentSale.objects.create(
            name="Sale 2",
            quantity=2,
            total_amount=Decimal('2000.00'),
            milestone_structure=structure,
            project_start_date=date.today()
        )
        
        # Both sales should have the same milestone structure
        self.assertEqual(sale1.milestone_structure, structure)
        self.assertEqual(sale2.milestone_structure, structure)
        
        # But different payment amounts
        schedule1 = sale1.get_milestone_schedule()
        schedule2 = sale2.get_milestone_schedule()
        
        self.assertEqual(schedule1[0]['payment_amount'], 1000.0)
        self.assertEqual(schedule2[0]['payment_amount'], 2000.0)