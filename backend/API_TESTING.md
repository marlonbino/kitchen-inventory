# API Testing Guide

This document provides sample cURL commands to test all API endpoints.

**Base URL:** `http://localhost:8000/api`

## 1. Items API

### List all items
```bash
curl -X GET http://localhost:8000/api/items/
```

### List items with filtering (by category)
```bash
curl -X GET "http://localhost:8000/api/items/?category=Produce"
```

### List items with filtering (by unit)
```bash
curl -X GET "http://localhost:8000/api/items/?unit=kg"
```

### Search items by name
```bash
curl -X GET "http://localhost:8000/api/items/?search=tomato"
```

### Order items by current_stock
```bash
curl -X GET "http://localhost:8000/api/items/?ordering=-current_stock"
```

### Get specific item
```bash
curl -X GET http://localhost:8000/api/items/1/
```

### Create new item
```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Potatoes",
    "category": "Produce",
    "unit": "kg",
    "min_stock_level": 20,
    "current_stock": 50
  }'
```

### Update item
```bash
curl -X PUT http://localhost:8000/api/items/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tomatoes Updated",
    "category": "Produce",
    "unit": "kg",
    "min_stock_level": 15,
    "current_stock": 30
  }'
```

### Partial update item
```bash
curl -X PATCH http://localhost:8000/api/items/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "current_stock": 35
  }'
```

### Delete item
```bash
curl -X DELETE http://localhost:8000/api/items/1/
```

## 2. Stock Movements API

### List all stock movements
```bash
curl -X GET http://localhost:8000/api/stock-movements/
```

### Filter by movement type
```bash
curl -X GET "http://localhost:8000/api/stock-movements/?movement_type=receipt"
```

### Filter by item
```bash
curl -X GET "http://localhost:8000/api/stock-movements/?item=1"
```

### Get specific stock movement
```bash
curl -X GET http://localhost:8000/api/stock-movements/1/
```

### Create stock movement (receipt - adds stock)
```bash
curl -X POST http://localhost:8000/api/stock-movements/ \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "movement_type": "receipt",
    "quantity": 10,
    "notes": "Stock received from supplier",
    "reference": "PO-12345"
  }'
```

### Create stock movement (issue - subtracts stock)
```bash
curl -X POST http://localhost:8000/api/stock-movements/ \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "movement_type": "issue",
    "quantity": 5,
    "notes": "Issued to kitchen",
    "reference": "ISSUE-001"
  }'
```

### Create stock movement (writeoff - subtracts stock)
```bash
curl -X POST http://localhost:8000/api/stock-movements/ \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "movement_type": "writeoff",
    "quantity": 2,
    "notes": "Expired items",
    "reference": "WO-001"
  }'
```

### Update stock movement
```bash
curl -X PUT http://localhost:8000/api/stock-movements/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "movement_type": "receipt",
    "quantity": 15,
    "notes": "Updated notes",
    "reference": "PO-12345-UPDATED"
  }'
```

### Delete stock movement
```bash
curl -X DELETE http://localhost:8000/api/stock-movements/1/
```

## 3. Requisitions API

### List all requisitions
```bash
curl -X GET http://localhost:8000/api/requisitions/
```

### Filter by status
```bash
curl -X GET "http://localhost:8000/api/requisitions/?status=pending"
```

### Filter by item
```bash
curl -X GET "http://localhost:8000/api/requisitions/?item=1"
```

### Get specific requisition
```bash
curl -X GET http://localhost:8000/api/requisitions/1/
```

### Create new requisition
```bash
curl -X POST http://localhost:8000/api/requisitions/ \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "quantity_requested": 20,
    "requested_by": "Chef John"
  }'
```

### Approve requisition (custom action)
```bash
curl -X POST http://localhost:8000/api/requisitions/1/approve/
```

### Reject requisition (custom action)
```bash
curl -X POST http://localhost:8000/api/requisitions/1/reject/
```

### Update requisition
```bash
curl -X PUT http://localhost:8000/api/requisitions/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "quantity_requested": 25,
    "requested_by": "Chef John",
    "status": "pending"
  }'
```

### Delete requisition
```bash
curl -X DELETE http://localhost:8000/api/requisitions/1/
```

## 4. Low Stock Items API

### Get all low stock items
```bash
curl -X GET http://localhost:8000/api/low-stock/
```

## 5. Dashboard Stats API

### Get dashboard statistics
```bash
curl -X GET http://localhost:8000/api/dashboard-stats/
```

Expected response structure:
```json
{
  "total_items": 10,
  "low_stock_count": 3,
  "pending_requisitions": 2,
  "recent_movements": [...],
  "total_stock_value": 350
}
```

## 6. Pagination

### Get items with pagination (page 2)
```bash
curl -X GET "http://localhost:8000/api/items/?page=2"
```

### Get items with custom page size
```bash
curl -X GET "http://localhost:8000/api/items/?page_size=10"
```

## 7. Combined Filters

### Filter items by category and search by name
```bash
curl -X GET "http://localhost:8000/api/items/?category=Produce&search=tomato"
```

### Get stock movements ordered by date (descending)
```bash
curl -X GET "http://localhost:8000/api/stock-movements/?ordering=-date"
```

## Notes

- All endpoints use JSON content type for POST/PUT/PATCH requests
- Pagination is set to 20 items per page by default
- Filtering, searching, and ordering are available where specified
- Stock movements automatically update item stock levels via signals
- The low-stock endpoint returns items where `current_stock < min_stock_level`
- Dashboard stats endpoint provides aggregated data for the inventory dashboard

