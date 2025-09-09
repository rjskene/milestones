from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta
from milestones.models import PaymentMilestoneStructure, PaymentMilestone
from .models import EquipmentSale


class EquipmentSaleAPITest(APITestCase):
    """Test cases for EquipmentSale API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        # Create a milestone structure
        self.structure = PaymentMilestoneStructure.objects.create(
            name='Test Structure',
            description='A test milestone structure'
        )
        
        # Create milestones
        self.milestone1 = PaymentMilestone.objects.create(
            structure=self.structure,
            name='Down Payment',
            payment_percentage=Decimal('30.00'),
            net_terms_days=0,
            days_after_previous=0,
            order=0
        )
        
        self.milestone2 = PaymentMilestone.objects.create(
            structure=self.structure,
            name='Final Payment',
            payment_percentage=Decimal('70.00'),
            net_terms_days=30,
            days_after_previous=30,
            order=1
        )
        
        self.sale_data = {
            'name': 'Test Equipment Sale',
            'vendor': 'Test Vendor',
            'quantity': 5,
            'total_amount': 100000.00,
            'milestone_structure_id': self.structure.id,
            'project_start_date': date.today().isoformat()
        }
    
    def test_create_equipment_sale(self):
        """Test creating a new equipment sale."""
        url = reverse('equipmentsale-list')
        response = self.client.post(url, self.sale_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EquipmentSale.objects.count(), 1)
        
        sale = EquipmentSale.objects.get()
        self.assertEqual(sale.name, 'Test Equipment Sale')
        self.assertEqual(sale.vendor, 'Test Vendor')
        self.assertEqual(sale.quantity, 5)
        self.assertEqual(sale.total_amount, Decimal('100000.00'))
        self.assertEqual(sale.milestone_structure, self.structure)
        self.assertEqual(sale.project_start_date, date.today())
    
    def test_create_equipment_sale_without_vendor(self):
        """Test creating an equipment sale without vendor."""
        sale_data = self.sale_data.copy()
        del sale_data['vendor']
        
        url = reverse('equipmentsale-list')
        response = self.client.post(url, sale_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        sale = EquipmentSale.objects.get()
        self.assertEqual(sale.vendor, '')
    
    def test_create_equipment_sale_invalid_quantity(self):
        """Test creating an equipment sale with invalid quantity."""
        sale_data = self.sale_data.copy()
        sale_data['quantity'] = 0  # Invalid quantity
        
        url = reverse('equipmentsale-list')
        response = self.client.post(url, sale_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EquipmentSale.objects.count(), 0)
    
    def test_create_equipment_sale_invalid_total_amount(self):
        """Test creating an equipment sale with invalid total amount."""
        sale_data = self.sale_data.copy()
        sale_data['total_amount'] = -1000.00  # Invalid amount
        
        url = reverse('equipmentsale-list')
        response = self.client.post(url, sale_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EquipmentSale.objects.count(), 0)
    
    def test_list_equipment_sales(self):
        """Test listing equipment sales."""
        # Create test sales
        sale1 = EquipmentSale.objects.create(
            name='Sale 1',
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        sale2 = EquipmentSale.objects.create(
            name='Sale 2',
            quantity=2,
            total_amount=Decimal('2000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        
        url = reverse('equipmentsale-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should be ordered by creation date (newest first)
        self.assertEqual(response.data[0]['name'], 'Sale 2')
        self.assertEqual(response.data[1]['name'], 'Sale 1')
    
    def test_retrieve_equipment_sale(self):
        """Test retrieving a specific equipment sale."""
        sale = EquipmentSale.objects.create(
            name='Test Sale',
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        
        url = reverse('equipmentsale-detail', kwargs={'pk': sale.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Sale')
        self.assertEqual(response.data['quantity'], 1)
        self.assertEqual(response.data['total_amount'], '1000.00')
        self.assertEqual(response.data['unit_price'], 1000.0)
    
    def test_update_equipment_sale(self):
        """Test updating an equipment sale."""
        sale = EquipmentSale.objects.create(
            name='Original Name',
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        
        update_data = {
            'name': 'Updated Name',
            'vendor': 'Updated Vendor',
            'quantity': 3,
            'total_amount': 3000.00,
            'milestone_structure_id': self.structure.id,
            'project_start_date': date.today().isoformat()
        }
        
        url = reverse('equipmentsale-detail', kwargs={'pk': sale.pk})
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        sale.refresh_from_db()
        self.assertEqual(sale.name, 'Updated Name')
        self.assertEqual(sale.vendor, 'Updated Vendor')
        self.assertEqual(sale.quantity, 3)
        self.assertEqual(sale.total_amount, Decimal('3000.00'))
    
    def test_delete_equipment_sale(self):
        """Test deleting an equipment sale."""
        sale = EquipmentSale.objects.create(
            name='To Delete',
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        
        url = reverse('equipmentsale-detail', kwargs={'pk': sale.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EquipmentSale.objects.count(), 0)
    
    def test_equipment_sale_schedule_endpoint(self):
        """Test the equipment sale schedule endpoint."""
        sale = EquipmentSale.objects.create(
            name='Schedule Test Sale',
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date(2024, 1, 1)
        )
        
        url = reverse('equipmentsale-schedule', kwargs={'pk': sale.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertEqual(data['name'], 'Schedule Test Sale')
        self.assertIn('milestone_schedule', data)
        
        schedule = data['milestone_schedule']
        self.assertEqual(len(schedule), 2)
        
        # Test first milestone
        first_milestone = schedule[0]
        self.assertEqual(first_milestone['name'], 'Down Payment')
        self.assertEqual(first_milestone['payment_amount'], 300.0)
        self.assertEqual(first_milestone['payment_percentage'], 30.0)
        
        # Test second milestone
        second_milestone = schedule[1]
        self.assertEqual(second_milestone['name'], 'Final Payment')
        self.assertEqual(second_milestone['payment_amount'], 700.0)
        self.assertEqual(second_milestone['payment_percentage'], 70.0)
    
    def test_equipment_sale_schedules_endpoint(self):
        """Test the equipment sale schedules endpoint (all sales)."""
        sale1 = EquipmentSale.objects.create(
            name='Sale 1',
            quantity=1,
            total_amount=Decimal('1000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        sale2 = EquipmentSale.objects.create(
            name='Sale 2',
            quantity=2,
            total_amount=Decimal('2000.00'),
            milestone_structure=self.structure,
            project_start_date=date.today()
        )
        
        url = reverse('equipmentsale-schedules')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Both should have milestone_schedule data
        for sale_data in response.data:
            self.assertIn('milestone_schedule', sale_data)
            self.assertEqual(len(sale_data['milestone_schedule']), 2)
    
    def test_equipment_sale_schedule_nonexistent_sale(self):
        """Test schedule endpoint with nonexistent sale."""
        url = reverse('equipmentsale-schedule', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_equipment_sale_with_complex_milestone_structure(self):
        """Test equipment sale with complex milestone structure."""
        # Create a complex milestone structure
        complex_structure = PaymentMilestoneStructure.objects.create(
            name='Complex Structure',
            description='A complex milestone structure'
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
                structure=complex_structure,
                name=data['name'],
                payment_percentage=Decimal(str(data['percentage'])),
                net_terms_days=data['net_terms'],
                days_after_previous=data['days'],
                order=i
            )
        
        # Create equipment sale
        sale_data = {
            'name': 'Complex Equipment Sale',
            'vendor': 'Complex Vendor',
            'quantity': 10,
            'total_amount': 500000.00,
            'milestone_structure_id': complex_structure.id,
            'project_start_date': date(2024, 1, 1).isoformat()
        }
        
        url = reverse('equipmentsale-list')
        response = self.client.post(url, sale_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        sale = EquipmentSale.objects.get()
        self.assertEqual(sale.name, 'Complex Equipment Sale')
        self.assertEqual(sale.quantity, 10)
        self.assertEqual(sale.total_amount, Decimal('500000.00'))
        
        # Test schedule generation
        schedule = sale.get_milestone_schedule()
        self.assertEqual(len(schedule), 4)
        
        # Verify payment amounts
        expected_amounts = [100000, 150000, 150000, 100000]  # 20%, 30%, 30%, 20%
        for i, milestone in enumerate(schedule):
            self.assertEqual(milestone['payment_amount'], expected_amounts[i])
