from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import F
from datetime import timedelta
from inventory.models import Item, StockMovement, Requisition


class Command(BaseCommand):
    help = 'Populates the database with minimal test data: 5 items, 10 stock movements, 3 requisitions. Ensures at least one low-stock item.'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate test data...')

        # Clear existing data
        self.stdout.write('Clearing existing test data...')
        StockMovement.objects.all().delete()
        Requisition.objects.all().delete()
        Item.objects.all().delete()

        # Create exactly 5 Items with variety across categories, units, and stock levels
        # Initial stocks set to account for movements that will be applied via signals
        items_data = [
            # Item 1: Produce - Low stock (below min_stock_level)
            # Final after movements: 0 + 25 - 12 - 5 = 8 (min=20, so LOW STOCK)
            {
                'name': 'Tomatoes',
                'category': 'Produce',
                'unit': 'kg',
                'min_stock_level': 20,
                'current_stock': 0
            },
            # Item 2: Dairy - Normal stock
            # Final: 45 + 50 - 15 + 20 = 100 (well above min=30)
            {
                'name': 'Milk',
                'category': 'Dairy',
                'unit': 'bottle',
                'min_stock_level': 30,
                'current_stock': 45
            },
            # Item 3: Pantry - Normal stock
            # Final: 75 + 100 - 25 = 150 (well above min=50)
            {
                'name': 'Rice',
                'category': 'Pantry',
                'unit': 'kg',
                'min_stock_level': 50,
                'current_stock': 75
            },
            # Item 4: Meat - Will be low stock after movements
            # Final: 20 - 8 = 12 (min=15, so LOW STOCK)
            {
                'name': 'Chicken Breast',
                'category': 'Meat',
                'unit': 'kg',
                'min_stock_level': 15,
                'current_stock': 20
            },
            # Item 5: Spices - Normal stock with different unit
            # Final: 700 - 50 = 650 (well above min=500)
            {
                'name': 'Black Pepper',
                'category': 'Spices',
                'unit': 'g',
                'min_stock_level': 500,
                'current_stock': 700
            }
        ]

        items = []
        for item_data in items_data:
            item = Item.objects.create(**item_data)
            items.append(item)
            self.stdout.write(self.style.SUCCESS(f'Created item: {item.name} (Stock: {item.current_stock} {item.unit}, Min: {item.min_stock_level})'))

        self.stdout.write(f'✓ Created {len(items)} items')
        
        # Verify at least one low stock item
        low_stock_items = [item for item in items if item.is_low_stock]
        if low_stock_items:
            self.stdout.write(self.style.WARNING(f'Low stock item detected: {low_stock_items[0].name}'))
        else:
            self.stdout.write(self.style.ERROR('Warning: No low stock items created!'))

        # Create exactly 10 Stock Movements across those items
        # We'll bypass signals for initial stock setup, then apply movements correctly
        base_date = timezone.now() - timedelta(days=14)

        movements_data = [
            # Receipts (increase stock)
            {'item': items[0], 'type': 'receipt', 'quantity': 25, 'notes': 'Initial stock receipt', 'ref': 'REC-001', 'days_ago': 14},
            {'item': items[1], 'type': 'receipt', 'quantity': 50, 'notes': 'Weekly delivery', 'ref': 'REC-002', 'days_ago': 12},
            {'item': items[2], 'type': 'receipt', 'quantity': 100, 'notes': 'Bulk purchase', 'ref': 'REC-003', 'days_ago': 10},
            
            # Issues (decrease stock) - must respect current stock
            {'item': items[1], 'type': 'issue', 'quantity': 15, 'notes': 'Kitchen usage', 'ref': 'ISS-001', 'days_ago': 8},
            {'item': items[0], 'type': 'issue', 'quantity': 12, 'notes': 'Daily prep', 'ref': 'ISS-002', 'days_ago': 6},
            {'item': items[2], 'type': 'issue', 'quantity': 25, 'notes': 'Meal preparation', 'ref': 'ISS-003', 'days_ago': 5},
            {'item': items[3], 'type': 'issue', 'quantity': 8, 'notes': 'Dinner service', 'ref': 'ISS-004', 'days_ago': 4},
            
            # Write-offs (decrease stock)
            {'item': items[0], 'type': 'writeoff', 'quantity': 5, 'notes': 'Spoilage - expired', 'ref': 'WO-001', 'days_ago': 3},
            {'item': items[4], 'type': 'writeoff', 'quantity': 50, 'notes': 'Damaged packaging', 'ref': 'WO-002', 'days_ago': 2},
            {'item': items[1], 'type': 'receipt', 'quantity': 20, 'notes': 'Restock delivery', 'ref': 'REC-004', 'days_ago': 1}
        ]

        # Create movements - signals will update stock automatically
        movements_created = 0
        for move_data in movements_data:
            # Calculate date based on days ago
            move_date = base_date + timedelta(days=move_data['days_ago'])
            
            # Create movement - signals will handle stock updates
            movement = StockMovement.objects.create(
                item=move_data['item'],
                movement_type=move_data['type'],
                quantity=move_data['quantity'],
                notes=move_data['notes'],
                reference=move_data['ref'],
                date=move_date
            )
            movements_created += 1

        self.stdout.write(f'✓ Created {movements_created} stock movements')

        # Create exactly 3 Requisitions with different statuses
        requisitions_data = [
            {
                'item': items[0],  # Tomatoes - low stock
                'quantity': 40,
                'requested_by': 'Chef John',
                'status': 'pending',
                'days_ago': 2
            },
            {
                'item': items[3],  # Chicken Breast
                'quantity': 25,
                'requested_by': 'Sous Chef Sarah',
                'status': 'approved',
                'days_ago': 5
            },
            {
                'item': items[2],  # Rice
                'quantity': 50,
                'requested_by': 'Manager Mike',
                'status': 'rejected',
                'days_ago': 7
            }
        ]

        requisitions_created = 0
        for req_data in requisitions_data:
            req_date = base_date + timedelta(days=req_data['days_ago'])
            
            requisition = Requisition.objects.create(
                item=req_data['item'],
                quantity_requested=req_data['quantity'],
                requested_by=req_data['requested_by'],
                status=req_data['status'],
                date_requested=req_date,
                date_processed=timezone.now() if req_data['status'] != 'pending' else None
            )
            requisitions_created += 1
            self.stdout.write(self.style.SUCCESS(f'Created requisition: {req_data["item"].name} - {req_data["status"]} by {req_data["requested_by"]}'))

        self.stdout.write(f'✓ Created {requisitions_created} requisitions')

        # Final summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Test data population completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  • Items: {Item.objects.count()}')
        self.stdout.write(f'  • Stock Movements: {StockMovement.objects.count()}')
        self.stdout.write(f'  • Requisitions: {Requisition.objects.count()}')
        
        # Check low stock items
        low_stock = Item.objects.filter(current_stock__lt=F('min_stock_level'))
        if low_stock.exists():
            self.stdout.write(f'\n  • Low Stock Items: {low_stock.count()}')
            for item in low_stock:
                self.stdout.write(self.style.WARNING(f'    ⚠️  {item.name}: {item.current_stock} {item.unit} (min: {item.min_stock_level})'))
        else:
            self.stdout.write(self.style.WARNING('\n  ⚠️  No low stock items found!'))
        
        self.stdout.write('\n')

