from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from inventory.models import Item, StockMovement, Requisition


class Command(BaseCommand):
    help = 'Populates the database with sample items, stock movements, and requisitions. Idempotent - can be run multiple times safely.'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate sample data...')

        # Clear existing data if it exists (for idempotency)
        self.stdout.write('Clearing existing sample data...')
        StockMovement.objects.all().delete()
        Requisition.objects.all().delete()
        Item.objects.all().delete()

        # Create Items (15-20 items across different categories)
        items_data = [
            # Produce
            {'name': 'Tomatoes', 'category': 'Produce', 'unit': 'kg', 'min_stock_level': 20, 'current_stock': 35},
            {'name': 'Onions', 'category': 'Produce', 'unit': 'kg', 'min_stock_level': 15, 'current_stock': 5},
            {'name': 'Potatoes', 'category': 'Produce', 'unit': 'kg', 'min_stock_level': 30, 'current_stock': 45},
            {'name': 'Carrots', 'category': 'Produce', 'unit': 'kg', 'min_stock_level': 10, 'current_stock': 12},
            {'name': 'Bell Peppers', 'category': 'Produce', 'unit': 'kg', 'min_stock_level': 8, 'current_stock': 3},
            {'name': 'Lettuce', 'category': 'Produce', 'unit': 'piece', 'min_stock_level': 20, 'current_stock': 25},
            
            # Dairy
            {'name': 'Milk', 'category': 'Dairy', 'unit': 'bottle', 'min_stock_level': 30, 'current_stock': 40},
            {'name': 'Cheese', 'category': 'Dairy', 'unit': 'kg', 'min_stock_level': 10, 'current_stock': 15},
            {'name': 'Yogurt', 'category': 'Dairy', 'unit': 'bottle', 'min_stock_level': 20, 'current_stock': 18},
            {'name': 'Butter', 'category': 'Dairy', 'unit': 'kg', 'min_stock_level': 5, 'current_stock': 2},
            {'name': 'Eggs', 'category': 'Dairy', 'unit': 'piece', 'min_stock_level': 60, 'current_stock': 80},
            
            # Pantry
            {'name': 'Rice', 'category': 'Pantry', 'unit': 'kg', 'min_stock_level': 50, 'current_stock': 75},
            {'name': 'Flour', 'category': 'Pantry', 'unit': 'kg', 'min_stock_level': 25, 'current_stock': 30},
            {'name': 'Sugar', 'category': 'Pantry', 'unit': 'kg', 'min_stock_level': 20, 'current_stock': 35},
            {'name': 'Olive Oil', 'category': 'Pantry', 'unit': 'bottle', 'min_stock_level': 15, 'current_stock': 20},
            {'name': 'Pasta', 'category': 'Pantry', 'unit': 'pack', 'min_stock_level': 40, 'current_stock': 55},
            
            # Meat
            {'name': 'Chicken Breast', 'category': 'Meat', 'unit': 'kg', 'min_stock_level': 20, 'current_stock': 15},
            {'name': 'Ground Beef', 'category': 'Meat', 'unit': 'kg', 'min_stock_level': 15, 'current_stock': 10},
            
            # Spices
            {'name': 'Salt', 'category': 'Spices', 'unit': 'kg', 'min_stock_level': 25, 'current_stock': 30},
            {'name': 'Black Pepper', 'category': 'Spices', 'unit': 'g', 'min_stock_level': 500, 'current_stock': 200},
            
            # Frozen
            {'name': 'Frozen Peas', 'category': 'Frozen', 'unit': 'pack', 'min_stock_level': 30, 'current_stock': 40},
            {'name': 'Frozen Corn', 'category': 'Frozen', 'unit': 'pack', 'min_stock_level': 25, 'current_stock': 30},
        ]

        items = []
        for item_data in items_data:
            item, created = Item.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            items.append(item)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created item: {item.name}'))

        self.stdout.write(f'Created/Verified {len(items)} items')

        # Create Stock Movements (30-40 movements)
        movement_types = ['receipt', 'issue', 'writeoff']
        movements_created = 0
        base_date = timezone.now() - timedelta(days=30)

        for i in range(35):
            item = random.choice(items)
            movement_type = random.choice(movement_types)
            
            # Generate quantity based on movement type
            if movement_type == 'receipt':
                quantity = random.randint(5, 50)
            else:
                quantity = random.randint(1, min(10, item.current_stock // 2 or 5))

            date = base_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            
            movement = StockMovement.objects.create(
                item=item,
                movement_type=movement_type,
                quantity=quantity,
                notes=f'Sample {movement_type} movement #{i+1}',
                reference=f'{movement_type.upper()}-{i+1:04d}',
                date=date
            )
            
            # Manually update item stock for movements (since we're creating them directly)
            if movement_type == 'receipt':
                item.current_stock += quantity
            else:
                item.current_stock = max(0, item.current_stock - quantity)
            item.save()
            
            movements_created += 1

        self.stdout.write(f'Created {movements_created} stock movements')

        # Create Requisitions (5-10 with mixed statuses)
        statuses = ['pending', 'approved', 'rejected']
        requisitions_created = 0
        requested_by_names = ['Chef John', 'Chef Sarah', 'Manager Mike', 'Sous Chef Lisa', 'Kitchen Staff']

        for i in range(8):
            item = random.choice(items)
            status = random.choice(statuses)
            quantity_requested = random.randint(5, 30)
            requested_by = random.choice(requested_by_names)
            
            date_requested = base_date + timedelta(days=random.randint(0, 30))
            
            requisition = Requisition.objects.create(
                item=item,
                quantity_requested=quantity_requested,
                requested_by=requested_by,
                status=status,
                date_requested=date_requested,
                date_processed=timezone.now() if status != 'pending' else None
            )
            
            requisitions_created += 1

        self.stdout.write(f'Created {requisitions_created} requisitions')
        self.stdout.write(self.style.SUCCESS('\nSample data population completed successfully!'))

