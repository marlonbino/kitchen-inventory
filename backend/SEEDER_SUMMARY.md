# Kitchen Inventory Test Data Seeder - Quick Start

## 🎯 Deliverables Summary

Created comprehensive test data seeding tools for your Kitchen Inventory System:

### ✅ Management Command: `seed_test_data`
**Location**: `inventory/management/commands/seed_test_data.py`

**What it does**:
- Creates exactly **5 items** with variety across categories and units
- Creates exactly **10 stock movements** (receipts, issues, write-offs)
- Creates exactly **3 requisitions** with different statuses
- **Ensures 2 low-stock items** for UI testing (Tomatoes & Chicken Breast)
- Idempotent - safe to run multiple times
- Properly handles Django signals for automatic stock updates

### ✅ Django Fixture: `test_data_fixture.json`  
**Location**: `inventory/fixtures/test_data_fixture.json`

**What it does**:
- Provides 5 items as JSON fixture
- Alternative loading method via `python manage.py loaddata`
- Note: Fixtures only create Items (not movements/requisitions due to signal constraints)

### ✅ Documentation: `TEST_DATA_SEEDER.md`
**Location**: `TEST_DATA_SEEDER.md`

**What it covers**:
- Complete usage instructions
- Detailed data breakdown
- Frontend testing checklist
- Troubleshooting guide

---

## 🚀 Quick Start

### 1. Run the Management Command (Recommended)

```bash
cd kitchen-inventory/backend
python manage.py seed_test_data
```

**Expected output**:
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

### 2. Or Use Django Fixture (Alternative)

```bash
cd kitchen-inventory/backend
python manage.py loaddata inventory/fixtures/test_data_fixture.json
```

---

## 📊 Test Data Created

### Items (5 total)

| Item | Category | Unit | Final Stock | Min Level | Status |
|------|----------|------|-------------|-----------|--------|
| Tomatoes | Produce | kg | 8 | 20 | ⚠️ LOW |
| Milk | Dairy | bottle | 100 | 30 | ✅ OK |
| Rice | Pantry | kg | 150 | 50 | ✅ OK |
| Chicken Breast | Meat | kg | 12 | 15 | ⚠️ LOW |
| Black Pepper | Spices | g | 650 | 500 | ✅ OK |

### Stock Movements (10 total)

| Type | Quantity | Item | Reference | Notes |
|------|----------|------|-----------|-------|
| Receipt | 25 | Tomatoes | REC-001 | Initial stock receipt |
| Receipt | 50 | Milk | REC-002 | Weekly delivery |
| Receipt | 100 | Rice | REC-003 | Bulk purchase |
| Issue | 15 | Milk | ISS-001 | Kitchen usage |
| Issue | 12 | Tomatoes | ISS-002 | Daily prep |
| Issue | 25 | Rice | ISS-003 | Meal preparation |
| Issue | 8 | Chicken Breast | ISS-004 | Dinner service |
| Write-off | 5 | Tomatoes | WO-001 | Spoilage - expired |
| Write-off | 50 | Black Pepper | WO-002 | Damaged packaging |
| Receipt | 20 | Milk | REC-004 | Restock delivery |

### Requisitions (3 total)

| Item | Quantity | Status | Requested By | Date Status |
|------|----------|--------|--------------|-------------|
| Tomatoes | 40 kg | Pending | Chef John | 2 days ago |
| Chicken Breast | 25 kg | Approved | Sous Chef Sarah | 5 days ago |
| Rice | 50 kg | Rejected | Manager Mike | 7 days ago |

---

## 🧪 Frontend Features to Test

After seeding, you can fully exercise:

### ✅ Item Management
- View all 5 items with different categories/units
- Test category and unit filtering
- Search by item name
- View item details
- **Low stock alerts** (Tomatoes & Chicken Breast)

### ✅ Stock Movements
- View 10 entries in history
- Filter by type (receipt/issue/write-off)
- Filter by item and date range
- View details with notes and references

### ✅ Requisitions
- View 3 with different statuses
- Filter by status (Pending/Approved/Rejected)
- Search by item/requester
- Test approval/rejection workflow

### ✅ Dashboard
- Real-time statistics
- Low stock alerts section
- Recent stock movements
- Navigation to detailed views

### ✅ Low Stock Alerts
- Color-coded indicators
- Quick actions (create requisition, quick receipt)
- Batch requisition creation
- Filter and sort options

---

## 🔍 Key Features

### Automatic Stock Updates
Uses Django signals to automatically update stock levels when movements are created:
- Receipts: increase stock
- Issues: decrease stock (with negative prevention)
- Write-offs: decrease stock (with negative prevention)

### Realistic Test Data
- All fields populated (notes, references, dates, statuses)
- Historical dates spread over last 14 days
- Realistic quantities and stock levels
- Low stock scenarios included

### Idempotent
- Can be run multiple times safely
- Clears existing data before seeding
- Consistent output every time

---

## 📁 Files Created

```
kitchen-inventory/backend/
├── inventory/
│   ├── management/
│   │   └── commands/
│   │       ├── seed_test_data.py       # ✨ Main management command
│   │       └── populate_sample_data.py # Existing command (20+ items)
│   └── fixtures/
│       ├── test_data_fixture.json      # ✨ JSON fixture
│       └── initial_data.json           # Existing fixture
├── TEST_DATA_SEEDER.md                 # ✨ Complete documentation
└── SEEDER_SUMMARY.md                   # ✨ This file
```

---

## 🆚 Comparison with Existing Seeder

| Feature | `seed_test_data` (NEW) | `populate_sample_data` (Existing) |
|---------|------------------------|-----------------------------------|
| Items | 5 (exact) | 20+ items |
| Stock Movements | 10 (exact) | 35+ movements |
| Requisitions | 3 (exact) | 8+ requisitions |
| Low Stock Items | 2 guaranteed | Variable |
| Use Case | **Minimal, focused testing** | Extensive testing |
| Data Consistency | High (controlled) | Medium (random) |

---

## 🔧 Requirements

- Django 4.2+
- Virtual environment activated
- Dependencies installed: `pip install -r requirements.txt`
- Database migrated: `python manage.py migrate`

---

## 📚 Documentation

For complete details, troubleshooting, and advanced usage:
**See**: `TEST_DATA_SEEDER.md`

---

## ✅ Validation

Test data meets all requirements:
- ✅ Exactly 5 items with variety
- ✅ Exactly 10 stock movements (receipts, issues, write-offs)
- ✅ Exactly 3 requisitions (all statuses)
- ✅ At least one (actually 2!) low-stock items
- ✅ All model fields populated
- ✅ Django signals properly integrated
- ✅ Idempotent operation

**Ready for frontend UI testing! 🎉**

