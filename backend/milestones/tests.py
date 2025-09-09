from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal
from datetime import date, timedelta
from .models import PaymentMilestoneStructure, PaymentMilestone


class PaymentMilestoneStructureModelTest(TestCase):
    """Test cases for PaymentMilestoneStructure model."""
    
    def setUp(self):
        """Set up test data."""
        self.structure = PaymentMilestoneStructure.objects.create(
            name="Test Structure",
            description="A test milestone structure"
        )
    
    def test_str_representation(self):
        """Test string representation of PaymentMilestoneStructure."""
        self.assertEqual(str(self.structure), "Test Structure")
    
    def test_unique_name_constraint(self):
        """Test that milestone structure names must be unique."""
        with self.assertRaises(IntegrityError):
            PaymentMilestoneStructure.objects.create(
                name="Test Structure",
                description="Another structure with same name"
            )
    
    def test_ordering(self):
        """Test that structures are ordered by name."""
        structure2 = PaymentMilestoneStructure.objects.create(name="Another Structure")
        structure3 = PaymentMilestoneStructure.objects.create(name="Zebra Structure")
        
        structures = list(PaymentMilestoneStructure.objects.all())
        self.assertEqual(structures[0].name, "Another Structure")
        self.assertEqual(structures[1].name, "Test Structure")
        self.assertEqual(structures[2].name, "Zebra Structure")


class PaymentMilestoneModelTest(TestCase):
    """Test cases for PaymentMilestone model."""
    
    def setUp(self):
        """Set up test data."""
        self.structure = PaymentMilestoneStructure.objects.create(
            name="Test Structure",
            description="A test milestone structure"
        )
        
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
    
    def test_str_representation(self):
        """Test string representation of PaymentMilestone."""
        expected = "Test Structure - Down Payment"
        self.assertEqual(str(self.milestone1), expected)
    
    def test_ordering(self):
        """Test that milestones are ordered by structure and order."""
        milestones = list(PaymentMilestone.objects.all())
        self.assertEqual(milestones[0].name, "Down Payment")
        self.assertEqual(milestones[1].name, "Final Payment")
    
    def test_unique_together_constraint(self):
        """Test that order must be unique within a structure."""
        with self.assertRaises(IntegrityError):
            PaymentMilestone.objects.create(
                structure=self.structure,
                name="Duplicate Order",
                payment_percentage=Decimal('10.00'),
                net_terms_days=0,
                days_after_previous=0,
                order=0  # Same order as milestone1
            )
    
    def test_payment_percentage_validation(self):
        """Test payment percentage validation."""
        # Test negative percentage
        milestone = PaymentMilestone(
            structure=self.structure,
            name="Invalid",
            payment_percentage=Decimal('-10.00'),
            net_terms_days=0,
            days_after_previous=0,
            order=2
        )
        with self.assertRaises(ValidationError):
            milestone.full_clean()
        
        # Test percentage over 100
        milestone.payment_percentage = Decimal('150.00')
        with self.assertRaises(ValidationError):
            milestone.full_clean()
    
    def test_clean_method_total_percentage_validation(self):
        """Test that total payment percentages don't exceed 100%."""
        # Create a milestone that would make total exceed 100%
        milestone = PaymentMilestone(
            structure=self.structure,
            name="Excessive Payment",
            payment_percentage=Decimal('50.00'),  # This would make total 130%
            net_terms_days=0,
            days_after_previous=0,
            order=2
        )
        
        with self.assertRaises(ValidationError) as context:
            milestone.clean()
        
        self.assertIn("Total payment percentage cannot exceed 100%", str(context.exception))
    
    def test_clean_method_valid_total_percentage(self):
        """Test that valid total percentages pass validation."""
        milestone = PaymentMilestone(
            structure=self.structure,
            name="Valid Payment",
            payment_percentage=Decimal('20.00'),  # This would make total 100%
            net_terms_days=0,
            days_after_previous=0,
            order=2
        )
        
        # Should not raise any exception
        milestone.clean()
    
    def test_net_terms_days_default(self):
        """Test that net_terms_days defaults to 0."""
        milestone = PaymentMilestone.objects.create(
            structure=self.structure,
            name="Default Net Terms",
            payment_percentage=Decimal('10.00'),
            days_after_previous=0,
            order=2
        )
        self.assertEqual(milestone.net_terms_days, 0)
    
    def test_days_after_previous_default(self):
        """Test that days_after_previous defaults to 0."""
        milestone = PaymentMilestone.objects.create(
            structure=self.structure,
            name="Default Days",
            payment_percentage=Decimal('10.00'),
            order=2
        )
        self.assertEqual(milestone.days_after_previous, 0)


class PaymentMilestoneIntegrationTest(TestCase):
    """Integration tests for PaymentMilestone and PaymentMilestoneStructure."""
    
    def test_cascade_delete(self):
        """Test that deleting a structure deletes its milestones."""
        structure = PaymentMilestoneStructure.objects.create(name="To Delete")
        milestone = PaymentMilestone.objects.create(
            structure=structure,
            name="Milestone",
            payment_percentage=Decimal('100.00'),
            order=0
        )
        
        milestone_id = milestone.id
        structure.delete()
        
        # Milestone should be deleted
        self.assertFalse(PaymentMilestone.objects.filter(id=milestone_id).exists())
    
    def test_related_milestones_access(self):
        """Test accessing milestones through structure relationship."""
        structure = PaymentMilestoneStructure.objects.create(name="Test Structure")
        
        milestone1 = PaymentMilestone.objects.create(
            structure=structure,
            name="First",
            payment_percentage=Decimal('50.00'),
            order=0
        )
        
        milestone2 = PaymentMilestone.objects.create(
            structure=structure,
            name="Second",
            payment_percentage=Decimal('50.00'),
            order=1
        )
        
        milestones = structure.milestones.all()
        self.assertEqual(len(milestones), 2)
        self.assertIn(milestone1, milestones)
        self.assertIn(milestone2, milestones)