from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Item, StockMovement, Requisition


class ItemModelTest(TestCase):
    """Test cases for Item model."""
    
    def test_item_creation(self):
        """Test that an Item can be created successfully."""
        item = Item.objects.create(
            name='Test Item',
            category='Produce',
            unit='kg',
            min_stock_level=10,
            current_stock=20
        )
        
        self.assertEqual(item.name, 'Test Item')
        self.assertEqual(item.category, 'Produce')
        self.assertEqual(item.unit, 'kg')
        self.assertEqual(item.min_stock_level, 10)
        self.assertEqual(item.current_stock, 20)
        self.assertIsNotNone(item.created_at)
        self.assertIsNotNone(item.updated_at)
    
    def test_item_is_low_stock_property(self):
        """Test the is_low_stock property returns True when stock is below minimum."""
        item = Item.objects.create(
            name='Low Stock Item',
            category='Dairy',
            unit='bottle',
            min_stock_level=10,
            current_stock=5
        )
        
        self.assertTrue(item.is_low_stock)
        
        # Update stock to above minimum
        item.current_stock = 15
        item.save()
        self.assertFalse(item.is_low_stock)
        
        # Edge case: stock equals minimum
        item.current_stock = 10
        item.save()
        self.assertFalse(item.is_low_stock)


class StockMovementSignalTest(TestCase):
    """Test cases for StockMovement signals that update item stock."""
    
    def setUp(self):
        """Create a test item for use in movement tests."""
        self.item = Item.objects.create(
            name='Test Item',
            category='Pantry',
            unit='kg',
            min_stock_level=10,
            current_stock=50
        )
    
    def test_receipt_movement_increases_stock(self):
        """Test that a receipt movement increases item stock."""
        initial_stock = self.item.current_stock
        
        movement = StockMovement.objects.create(
            item=self.item,
            movement_type='receipt',
            quantity=20,
            notes='Test receipt',
            reference='REC-001'
        )
        
        # Refresh item from database
        self.item.refresh_from_db()
        
        self.assertEqual(self.item.current_stock, initial_stock + 20)
        self.assertEqual(movement.quantity, 20)
    
    def test_issue_movement_decreases_stock(self):
        """Test that an issue movement decreases item stock."""
        initial_stock = self.item.current_stock
        
        movement = StockMovement.objects.create(
            item=self.item,
            movement_type='issue',
            quantity=15,
            notes='Test issue',
            reference='ISS-001'
        )
        
        # Refresh item from database
        self.item.refresh_from_db()
        
        self.assertEqual(self.item.current_stock, initial_stock - 15)
        self.assertEqual(movement.quantity, 15)
    
    def test_writeoff_movement_decreases_stock(self):
        """Test that a writeoff movement decreases item stock."""
        initial_stock = self.item.current_stock
        
        movement = StockMovement.objects.create(
            item=self.item,
            movement_type='writeoff',
            quantity=10,
            notes='Test writeoff',
            reference='WOF-001'
        )
        
        # Refresh item from database
        self.item.refresh_from_db()
        
        self.assertEqual(self.item.current_stock, initial_stock - 10)
        self.assertEqual(movement.quantity, 10)
    
    def test_negative_stock_prevention_on_issue(self):
        """Test that issuing more than available stock raises ValidationError."""
        # Set stock to a low value
        self.item.current_stock = 5
        self.item.save()
        
        # Try to issue more than available
        with self.assertRaises(ValidationError):
            StockMovement.objects.create(
                item=self.item,
                movement_type='issue',
                quantity=10,  # More than available stock
                notes='Should fail',
                reference='ISS-FAIL'
            )
        
        # Verify stock hasn't changed
        self.item.refresh_from_db()
        self.assertEqual(self.item.current_stock, 5)
    
    def test_negative_stock_prevention_on_writeoff(self):
        """Test that writing off more than available stock raises ValidationError."""
        # Set stock to a low value
        self.item.current_stock = 3
        self.item.save()
        
        # Try to writeoff more than available
        with self.assertRaises(ValidationError):
            StockMovement.objects.create(
                item=self.item,
                movement_type='writeoff',
                quantity=5,  # More than available stock
                notes='Should fail',
                reference='WOF-FAIL'
            )
        
        # Verify stock hasn't changed
        self.item.refresh_from_db()
        self.assertEqual(self.item.current_stock, 3)
    
    def test_multiple_movements_update_stock_correctly(self):
        """Test that multiple movements update stock correctly."""
        initial_stock = self.item.current_stock
        
        # Create multiple movements
        StockMovement.objects.create(
            item=self.item,
            movement_type='receipt',
            quantity=30,
            notes='Receipt 1'
        )
        
        StockMovement.objects.create(
            item=self.item,
            movement_type='issue',
            quantity=10,
            notes='Issue 1'
        )
        
        StockMovement.objects.create(
            item=self.item,
            movement_type='receipt',
            quantity=20,
            notes='Receipt 2'
        )
        
        StockMovement.objects.create(
            item=self.item,
            movement_type='writeoff',
            quantity=5,
            notes='Writeoff 1'
        )
        
        # Refresh item from database
        self.item.refresh_from_db()
        
        expected_stock = initial_stock + 30 - 10 + 20 - 5
        self.assertEqual(self.item.current_stock, expected_stock)


class RequisitionModelTest(TestCase):
    """Test cases for Requisition model."""
    
    def setUp(self):
        """Create a test item for requisition tests."""
        self.item = Item.objects.create(
            name='Test Item',
            category='Meat',
            unit='kg',
            min_stock_level=10,
            current_stock=20
        )
    
    def test_requisition_creation(self):
        """Test that a Requisition can be created successfully."""
        requisition = Requisition.objects.create(
            item=self.item,
            quantity_requested=15,
            requested_by='Chef John',
            status='pending'
        )
        
        self.assertEqual(requisition.item, self.item)
        self.assertEqual(requisition.quantity_requested, 15)
        self.assertEqual(requisition.requested_by, 'Chef John')
        self.assertEqual(requisition.status, 'pending')
        self.assertIsNotNone(requisition.date_requested)
        self.assertIsNone(requisition.date_processed)


class LowStockEndpointTest(TestCase):
    """Test cases for the low-stock endpoint functionality."""
    
    def setUp(self):
        """Create test items with different stock levels."""
        # Items with low stock
        self.low_stock_item1 = Item.objects.create(
            name='Low Stock Item 1',
            category='Dairy',
            unit='bottle',
            min_stock_level=20,
            current_stock=5  # Below minimum
        )
        
        self.low_stock_item2 = Item.objects.create(
            name='Low Stock Item 2',
            category='Produce',
            unit='kg',
            min_stock_level=30,
            current_stock=10  # Below minimum
        )
        
        # Item with adequate stock
        self.adequate_stock_item = Item.objects.create(
            name='Adequate Stock Item',
            category='Pantry',
            unit='kg',
            min_stock_level=10,
            current_stock=50  # Above minimum
        )
        
        # Item exactly at minimum (should not be low stock)
        self.at_minimum_item = Item.objects.create(
            name='At Minimum Item',
            category='Spices',
            unit='g',
            min_stock_level=100,
            current_stock=100  # Exactly at minimum
        )
    
    def test_low_stock_filter_returns_correct_items(self):
        """Test that filtering for low stock returns only items below minimum."""
        from django.db.models import F
        
        low_stock_items = Item.objects.filter(
            current_stock__lt=F('min_stock_level')
        )
        
        # Should return 2 items (low_stock_item1 and low_stock_item2)
        self.assertEqual(low_stock_items.count(), 2)
        
        # Verify correct items
        item_names = set(low_stock_items.values_list('name', flat=True))
        self.assertIn('Low Stock Item 1', item_names)
        self.assertIn('Low Stock Item 2', item_names)
        self.assertNotIn('Adequate Stock Item', item_names)
        self.assertNotIn('At Minimum Item', item_names)
    
    def test_is_low_stock_property_on_filtered_items(self):
        """Test that is_low_stock property works correctly on filtered items."""
        from django.db.models import F
        
        low_stock_items = Item.objects.filter(
            current_stock__lt=F('min_stock_level')
        )
        
        for item in low_stock_items:
            self.assertTrue(item.is_low_stock, f"{item.name} should be low stock")
        
        # Verify items not in filter are not low stock
        adequate_items = Item.objects.exclude(
            current_stock__lt=F('min_stock_level')
        )
        for item in adequate_items:
            self.assertFalse(item.is_low_stock, f"{item.name} should not be low stock")
