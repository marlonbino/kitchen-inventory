# Kitchen Inventory Test Data Seeder

This document describes the test data seeder commands available for the Kitchen Inventory System.

## Overview

The test data seeder provides two methods to populate your database with sample data for testing and development:

1. **Management Command**: `seed_test_data` (recommended)
2. **Django Fixture**: `test_data_fixture.json` (alternative)

## Management Command (Recommended)

### Command: `seed_test_data`

Creates exactly **5 items, 10 stock movements, and 3 requisitions** with realistic test data.

### Features

- ✅ Exactly 5 items across different categories (Produce, Dairy, Pantry, Meat, Spices)
- ✅ Exactly 10 stock movements (receipts, issues, write-offs) across items
- ✅ Exactly 3 requisitions with different statuses (pending, approved, rejected)
- ✅ At least one item with low stock (below `min_stock_level`) for alert testing
- ✅ Idempotent - can be run multiple times safely (clears existing data first)
- ✅ Handles stock updates automatically via Django signals

### Usage

```bash
cd kitchen-inventory/backend
python manage.py seed_test_data
```

### Output

The command provides detailed output including:

```
Starting to populate test data...
Clearing existing test data...
Created item: Tomatoes (Stock: 0 kg, Min: 20)
Created item: Milk (Stock: 45 bottle, Min: 30)
Created item: Rice (Stock: 75 kg, Min: 50)
Created item: Chicken Breast (Stock: 20 kg, Min: 15)
Created item: Black Pepper (Stock: 700 g, Min: 500)
✓ Created 5 items
Low stock item detected: Tomatoes
✓ Created 10 stock movements
✓ Created 3 requisitions

============================================================
Test data population completed successfully!
============================================================

Summary:
  • Items: 5
  • Stock Movements: 10
  • Requisitions: 3

  • Low Stock Items: 2
    ⚠️  Tomatoes: 8 kg (min: 20)
    ⚠️  Chicken Breast: 12 kg (min: 15)
```

### Test Data Details

#### Items Created (Final Stock Levels After Movements)

1. **Tomatoes** - Produce, kg - Stock: 8 (min: 20) ⚠️ **LOW STOCK**
2. **Milk** - Dairy, bottle - Stock: 100 (min: 30)
3. **Rice** - Pantry, kg - Stock: 150 (min: 50)
4. **Chicken Breast** - Meat, kg - Stock: 12 (min: 15) ⚠️ **LOW STOCK**
5. **Black Pepper** - Spices, g - Stock: 650 (min: 500)

#### Stock Movements

The seeder creates 10 movements:
- **Receipts**: Initial stock receipts, weekly deliveries, bulk purchases
- **Issues**: Kitchen usage, daily prep, meal preparation, dinner service
- **Write-offs**: Spoilage, damaged packaging

All movements include:
- Realistic notes
- Unique references (REC-001, ISS-001, WO-001, etc.)
- Dates spread over the last 14 days
- Automatic stock updates via Django signals

#### Requisitions

The seeder creates 3 requisitions:

1. **Pending**: Tomatoes (low stock) - 40 kg requested by Chef John
2. **Approved**: Chicken Breast - 25 kg requested by Sous Chef Sarah
3. **Rejected**: Rice - 50 kg requested by Manager Mike

## Django Fixture (Alternative)

### Fixture: `test_data_fixture.json`

Located at: `inventory/fixtures/test_data_fixture.json`

### Usage

```bash
cd kitchen-inventory/backend
python manage.py loaddata inventory/fixtures/test_data_fixture.json
```

**Note**: Fixtures only create Items, not movements or requisitions, as Django signals would interfere with historical data integrity. For complete test data including movements and requisitions, use the management command.

### Fixture Contents

The fixture includes 5 items with different categories and units:

1. **Tomatoes** - Produce, kg - Stock: 8 (min: 20) ⚠️ **LOW STOCK**
2. **Milk** - Dairy, bottle - Stock: 100 (min: 30)
3. **Rice** - Pantry, kg - Stock: 150 (min: 50)
4. **Chicken Breast** - Meat, kg - Stock: 12 (min: 15) ⚠️ **LOW STOCK**
5. **Black Pepper** - Spices, g - Stock: 650 (min: 500)

## Frontend Testing

After seeding, you can test the following UI features:

### ✅ Item Management
- View all 5 items with different categories and units
- Test category and unit filtering
- Search by item name
- View item details
- **Low stock alerts** (Tomatoes and Chicken Breast should trigger)

### ✅ Stock Movements
- View movement history with 10 entries
- Filter by movement type (receipt, issue, write-off)
- Filter by item
- View movement details with notes and references
- Test date range filtering

### ✅ Requisitions
- View all 3 requisitions with different statuses
- Filter by status (Pending, Approved, Rejected)
- Search by item or requester
- Test approval/rejection workflow
- View requisition details

### ✅ Dashboard
- Real-time statistics
- Low stock alerts section
- Recent stock movements
- Navigation to detailed views

### ✅ Low Stock Alerts
- Color-coded alerts (red/orange indicators)
- Quick actions (create requisition, quick receipt)
- Batch requisition creation
- Filter and sort options

## Comparison with `populate_sample_data`

The existing `populate_sample_data` command creates extensive data:
- 20+ items
- 35+ stock movements
- 8+ requisitions

The new `seed_test_data` command is optimized for **minimal, focused testing**:
- Exactly 5 items (sufficient for all feature testing)
- Exactly 10 movements (covers all movement types)
- Exactly 3 requisitions (covers all statuses)
- Ensures low stock scenarios

## Clearing Test Data

The `seed_test_data` command automatically clears existing data before seeding. If you need to clear manually:

```bash
python manage.py shell
```

```python
from inventory.models import Item, StockMovement, Requisition
StockMovement.objects.all().delete()
Requisition.objects.all().delete()
Item.objects.all().delete()
```

## Requirements

- Django 4.2+
- Virtual environment activated
- Dependencies installed: `pip install -r requirements.txt`
- Database migrated: `python manage.py migrate`

## Troubleshooting

### Command not found

If `seed_test_data` command is not found:

1. Ensure you're in the `kitchen-inventory/backend` directory
2. Check that the command file exists at `inventory/management/commands/seed_test_data.py`
3. Activate your virtual environment
4. Run `python manage.py help` to see all available commands

### Import errors

If you see import errors:

1. Activate your virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure `inventory` app is in `INSTALLED_APPS` in `settings.py`

### Signal errors

If you see validation errors about negative stock:

- This shouldn't happen with the seed command as it properly handles stock initialization
- Check that `inventory/signals.py` is being imported in `inventory/apps.py`
- Run migrations: `python manage.py migrate`

## Support

For questions or issues, please refer to the main project README or open an issue in the repository.

