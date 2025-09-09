from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import PaymentMilestoneStructure, PaymentMilestone


class PaymentMilestoneStructureAPITest(APITestCase):
    """Test cases for PaymentMilestoneStructure API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.structure_data = {
            'name': 'Test Structure',
            'description': 'A test milestone structure',
            'milestones': [
                {
                    'name': 'Down Payment',
                    'payment_percentage': 30.00,
                    'net_terms_days': 0,
                    'days_after_previous': 0,
                    'order': 0
                },
                {
                    'name': 'Final Payment',
                    'payment_percentage': 70.00,
                    'net_terms_days': 30,
                    'days_after_previous': 30,
                    'order': 1
                }
            ]
        }
    
    def test_create_milestone_structure(self):
        """Test creating a new milestone structure."""
        url = reverse('paymentmilestonestructure-list')
        response = self.client.post(url, self.structure_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PaymentMilestoneStructure.objects.count(), 1)
        
        structure = PaymentMilestoneStructure.objects.get()
        self.assertEqual(structure.name, 'Test Structure')
        self.assertEqual(structure.description, 'A test milestone structure')
        self.assertEqual(structure.milestones.count(), 2)
    
    def test_create_milestone_structure_duplicate_name(self):
        """Test creating a milestone structure with duplicate name."""
        # Create first structure
        PaymentMilestoneStructure.objects.create(name='Duplicate Name')
        
        # Try to create another with same name
        url = reverse('paymentmilestonestructure-list')
        response = self.client.post(url, self.structure_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PaymentMilestoneStructure.objects.count(), 1)
    
    def test_list_milestone_structures(self):
        """Test listing milestone structures."""
        # Create test structures
        structure1 = PaymentMilestoneStructure.objects.create(name='Structure 1')
        structure2 = PaymentMilestoneStructure.objects.create(name='Structure 2')
        
        url = reverse('paymentmilestonestructure-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Structure 1')
        self.assertEqual(response.data[1]['name'], 'Structure 2')
    
    def test_retrieve_milestone_structure(self):
        """Test retrieving a specific milestone structure."""
        structure = PaymentMilestoneStructure.objects.create(
            name='Test Structure',
            description='Test Description'
        )
        
        url = reverse('paymentmilestonestructure-detail', kwargs={'pk': structure.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Structure')
        self.assertEqual(response.data['description'], 'Test Description')
    
    def test_update_milestone_structure(self):
        """Test updating a milestone structure."""
        structure = PaymentMilestoneStructure.objects.create(
            name='Original Name',
            description='Original Description'
        )
        
        update_data = {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'milestones': [
                {
                    'name': 'Updated Milestone',
                    'payment_percentage': 100.00,
                    'net_terms_days': 0,
                    'days_after_previous': 0,
                    'order': 0
                }
            ]
        }
        
        url = reverse('paymentmilestonestructure-detail', kwargs={'pk': structure.pk})
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        structure.refresh_from_db()
        self.assertEqual(structure.name, 'Updated Name')
        self.assertEqual(structure.description, 'Updated Description')
        self.assertEqual(structure.milestones.count(), 1)
        self.assertEqual(structure.milestones.first().name, 'Updated Milestone')
    
    def test_delete_milestone_structure(self):
        """Test deleting a milestone structure."""
        structure = PaymentMilestoneStructure.objects.create(name='To Delete')
        
        url = reverse('paymentmilestonestructure-detail', kwargs={'pk': structure.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PaymentMilestoneStructure.objects.count(), 0)
    
    def test_create_milestone_structure_invalid_percentages(self):
        """Test creating a milestone structure with invalid payment percentages."""
        invalid_data = {
            'name': 'Invalid Structure',
            'description': 'Structure with invalid percentages',
            'milestones': [
                {
                    'name': 'Milestone 1',
                    'payment_percentage': 60.00,
                    'net_terms_days': 0,
                    'days_after_previous': 0,
                    'order': 0
                },
                {
                    'name': 'Milestone 2',
                    'payment_percentage': 60.00,  # Total would be 120%
                    'net_terms_days': 0,
                    'days_after_previous': 0,
                    'order': 1
                }
            ]
        }
        
        url = reverse('paymentmilestonestructure-list')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PaymentMilestoneStructure.objects.count(), 0)


class PaymentMilestoneAPITest(APITestCase):
    """Test cases for PaymentMilestone API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.structure = PaymentMilestoneStructure.objects.create(
            name='Test Structure',
            description='A test milestone structure'
        )
        
        self.milestone_data = {
            'structure': self.structure.id,
            'name': 'Test Milestone',
            'payment_percentage': 50.00,
            'net_terms_days': 15,
            'days_after_previous': 30,
            'order': 0
        }
    
    def test_create_milestone(self):
        """Test creating a new milestone."""
        url = reverse('paymentmilestone-list')
        response = self.client.post(url, self.milestone_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PaymentMilestone.objects.count(), 1)
        
        milestone = PaymentMilestone.objects.get()
        self.assertEqual(milestone.name, 'Test Milestone')
        self.assertEqual(milestone.payment_percentage, Decimal('50.00'))
        self.assertEqual(milestone.net_terms_days, 15)
        self.assertEqual(milestone.days_after_previous, 30)
    
    def test_list_milestones(self):
        """Test listing milestones."""
        # Create test milestones
        milestone1 = PaymentMilestone.objects.create(
            structure=self.structure,
            name='Milestone 1',
            payment_percentage=Decimal('50.00'),
            order=0
        )
        milestone2 = PaymentMilestone.objects.create(
            structure=self.structure,
            name='Milestone 2',
            payment_percentage=Decimal('50.00'),
            order=1
        )
        
        url = reverse('paymentmilestone-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_milestones_filtered_by_structure(self):
        """Test listing milestones filtered by structure."""
        # Create another structure
        structure2 = PaymentMilestoneStructure.objects.create(name='Structure 2')
        
        # Create milestones in both structures
        milestone1 = PaymentMilestone.objects.create(
            structure=self.structure,
            name='Milestone 1',
            payment_percentage=Decimal('100.00'),
            order=0
        )
        milestone2 = PaymentMilestone.objects.create(
            structure=structure2,
            name='Milestone 2',
            payment_percentage=Decimal('100.00'),
            order=0
        )
        
        url = reverse('paymentmilestone-list')
        response = self.client.get(url, {'structure_id': self.structure.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Milestone 1')
    
    def test_retrieve_milestone(self):
        """Test retrieving a specific milestone."""
        milestone = PaymentMilestone.objects.create(
            structure=self.structure,
            name='Test Milestone',
            payment_percentage=Decimal('100.00'),
            order=0
        )
        
        url = reverse('paymentmilestone-detail', kwargs={'pk': milestone.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Milestone')
    
    def test_update_milestone(self):
        """Test updating a milestone."""
        milestone = PaymentMilestone.objects.create(
            structure=self.structure,
            name='Original Name',
            payment_percentage=Decimal('50.00'),
            order=0
        )
        
        update_data = {
            'structure': self.structure.id,
            'name': 'Updated Name',
            'payment_percentage': 75.00,
            'net_terms_days': 30,
            'days_after_previous': 45,
            'order': 0
        }
        
        url = reverse('paymentmilestone-detail', kwargs={'pk': milestone.pk})
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        milestone.refresh_from_db()
        self.assertEqual(milestone.name, 'Updated Name')
        self.assertEqual(milestone.payment_percentage, Decimal('75.00'))
        self.assertEqual(milestone.net_terms_days, 30)
        self.assertEqual(milestone.days_after_previous, 45)
    
    def test_delete_milestone(self):
        """Test deleting a milestone."""
        milestone = PaymentMilestone.objects.create(
            structure=self.structure,
            name='To Delete',
            payment_percentage=Decimal('100.00'),
            order=0
        )
        
        url = reverse('paymentmilestone-detail', kwargs={'pk': milestone.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PaymentMilestone.objects.count(), 0)
