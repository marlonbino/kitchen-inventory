# BITZ Kitchen Inventory Backend

Django REST Framework API for the BITZ Kitchen Inventory Management System.

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- Django (>=4.2.0)
- Django REST Framework (>=3.14.0)
- django-cors-headers (>=4.0.0)
- python-decouple (>=3.8)
- django-filter (>=23.0)

4. Create `.env` file from `env.example`:
```bash
cp env.example .env
```

Edit `.env` file with your configuration (or leave defaults for development):
```
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. (Optional) Populate sample data:
```bash
python manage.py seed_test_data
```

This command creates:
- Admin user (username: `admin`, password: `p@ssw0rd`)
- Manager user (username: `manager`, password: `p@ssw0rd`)
- Staff user (username: `staff`, password: `p@ssw0rd`)
- Sample categories (Groceries, Meat, Dairy, Produce, etc.)
- 20+ sample items across different categories
- Sample stock movements (receipts, usage, waste)
- Sample requisitions with mixed statuses

**Note:** The command safely clears existing data and recreates sample data.

7. Create a superuser (if not exists):
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

Admin panel: `http://localhost:8000/admin/`

API Base URL: `http://localhost:8000/api/`

## Authentication

The API uses **Token Authentication**. Users must authenticate to access most endpoints.

### Login

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "p@ssw0rd"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@bitz.com",
    "role": "admin"
  }
}
```

### Using the Token

Include the token in the `Authorization` header for all subsequent requests:

```bash
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Logout

```bash
POST /api/auth/logout/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Get Current User

```bash
GET /api/auth/user/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## API Endpoints

All endpoints support pagination (20 items per page by default) and can be filtered/searched.

**Note:** Most endpoints require authentication. Include the token in the `Authorization` header.

### Items API

**Base URL:** `http://localhost:8000/api/items/`

#### List Items
```
GET /api/items/
```

**Query Parameters:**
- `category` - Filter by category (Produce, Dairy, Pantry, Meat, Spices, Frozen, Other)
- `unit` - Filter by unit (kg, g, lb, oz, piece, bottle, pack)
- `search` - Search by name
- `ordering` - Order by field (name, current_stock, min_stock_level)
- `page` - Page number for pagination
- `page_size` - Items per page (max 100)

**Example:**
```bash
# Get all items
curl http://localhost:8000/api/items/

# Filter by category
curl http://localhost:8000/api/items/?category=Dairy

# Search by name
curl http://localhost:8000/api/items/?search=tomato

# Order by current stock
curl http://localhost:8000/api/items/?ordering=-current_stock
```

**Response:**
```json
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Tomatoes",
      "category": "Produce",
      "unit": "kg",
      "min_stock_level": 20,
      "current_stock": 35,
      "is_low_stock": false,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

#### Create Item
```
POST /api/items/
```

**Request Body:**
```json
{
  "name": "Apples",
  "category": "Produce",
  "unit": "kg",
  "min_stock_level": 15,
  "current_stock": 25
}
```

#### Get Item Details
```
GET /api/items/{id}/
```

#### Update Item
```
PUT /api/items/{id}/
PATCH /api/items/{id}/
```

#### Delete Item
```
DELETE /api/items/{id}/
```

### Stock Movements API

**Base URL:** `http://localhost:8000/api/stock-movements/`

#### List Stock Movements
```
GET /api/stock-movements/
```

**Query Parameters:**
- `movement_type` - Filter by type (receipt, issue, writeoff)
- `item` - Filter by item ID
- `ordering` - Order by field (date, quantity)

**Example:**
```bash
# Get all movements
curl http://localhost:8000/api/stock-movements/

# Filter by type
curl http://localhost:8000/api/stock-movements/?movement_type=receipt

# Get movements for specific item
curl http://localhost:8000/api/stock-movements/?item=1
```

**Response:**
```json
{
  "count": 35,
  "results": [
    {
      "id": 1,
      "item": {
        "id": 1,
        "name": "Tomatoes"
      },
      "item_id": 1,
      "item_name": "Tomatoes",
      "movement_type": "receipt",
      "quantity": 20,
      "notes": "Sample receipt movement #1",
      "date": "2024-01-01T12:00:00Z",
      "reference": "REC-0001"
    }
  ]
}
```

#### Create Stock Movement
```
POST /api/stock-movements/
```

**Request Body:**
```json
{
  "item_id": 1,
  "movement_type": "receipt",
  "quantity": 25,
  "notes": "Received from supplier",
  "reference": "REC-001"
}
```

**Note:** 
- `receipt` increases stock
- `issue` decreases stock (validates against negative stock)
- `writeoff` decreases stock (validates against negative stock)

**Validation:** The API prevents creating movements that would result in negative stock for `issue` and `writeoff` types.

#### Get Stock Movement Details
```
GET /api/stock-movements/{id}/
```

#### Update Stock Movement
```
PUT /api/stock-movements/{id}/
PATCH /api/stock-movements/{id}/
```

#### Delete Stock Movement
```
DELETE /api/stock-movements/{id}/
```

### Requisitions API

**Base URL:** `http://localhost:8000/api/requisitions/`

#### List Requisitions
```
GET /api/requisitions/
```

**Query Parameters:**
- `status` - Filter by status (pending, approved, rejected)
- `item` - Filter by item ID
- `ordering` - Order by field (date_requested, date_processed)

**Example:**
```bash
# Get all requisitions
curl http://localhost:8000/api/requisitions/

# Filter by status
curl http://localhost:8000/api/requisitions/?status=pending

# Get requisitions for specific item
curl http://localhost:8000/api/requisitions/?item=1
```

**Response:**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "item": {
        "id": 1,
        "name": "Tomatoes"
      },
      "item_id": 1,
      "item_name": "Tomatoes",
      "quantity_requested": 15,
      "requested_by": "Chef John",
      "status": "pending",
      "date_requested": "2024-01-01T12:00:00Z",
      "date_processed": null
    }
  ]
}
```

#### Create Requisition
```
POST /api/requisitions/
```

**Request Body:**
```json
{
  "item_id": 1,
  "quantity_requested": 20,
  "requested_by": "Chef Sarah",
  "status": "pending"
}
```

#### Get Requisition Details
```
GET /api/requisitions/{id}/
```

#### Update Requisition
```
PUT /api/requisitions/{id}/
PATCH /api/requisitions/{id}/
```

#### Delete Requisition
```
DELETE /api/requisitions/{id}/
```

#### Approve Requisition
```
POST /api/requisitions/{id}/approve/
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/requisitions/1/approve/
```

#### Reject Requisition
```
POST /api/requisitions/{id}/reject/
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/requisitions/1/reject/
```

### Low Stock Endpoint

**Base URL:** `http://localhost:8000/api/low-stock/`

#### Get Low Stock Items
```
GET /api/low-stock/
```

Returns all items where `current_stock < min_stock_level`.

**Example:**
```bash
curl http://localhost:8000/api/low-stock/
```

**Response:**
```json
[
  {
    "id": 2,
    "name": "Onions",
    "category": "Produce",
    "unit": "kg",
    "min_stock_level": 15,
    "current_stock": 5,
    "is_low_stock": true,
    "shortage_amount": 10,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
]
```

### Dashboard Stats Endpoint

**Base URL:** `http://localhost:8000/api/dashboard-stats/`

#### Get Dashboard Statistics
```
GET /api/dashboard-stats/
```

Returns aggregated statistics for the inventory dashboard.

**Example:**
```bash
curl http://localhost:8000/api/dashboard-stats/
```

**Response:**
```json
{
  "total_items": 20,
  "low_stock_count": 3,
  "pending_requisitions": 2,
  "recent_movements": [
    {
      "id": 35,
      "item": {
        "id": 1,
        "name": "Tomatoes"
      },
      "movement_type": "receipt",
      "quantity": 10,
      "date": "2024-01-15T10:00:00Z"
    }
  ],
  "total_stock_value": 450
}
```

## Running Tests

To run the test suite:

```bash
python manage.py test inventory
```

This will run tests for:
- Item model creation and properties
- StockMovement signal updates (stock increases/decreases)
- Negative stock prevention validation
- Low stock filtering logic

## Frontend Integration

The backend API is designed to work with the Vue.js frontend application. 

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure API URL (optional, defaults to `http://localhost:8000/api`):
Create `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

4. Start the development server:
```bash
npm run dev
```

The frontend will typically run on `http://localhost:5173` (Vite default port).

### API Integration

- **Base URL**: `http://localhost:8000/api`
- **Content-Type**: `application/json`
- All endpoints return JSON
- Errors return appropriate HTTP status codes with error details

### User Management (Admin Only)

**Base URL:** `http://localhost:8000/api/admin/users/`

#### List All Users
```bash
GET /api/admin/users/
Authorization: Token <admin-token>
```

#### Create User
```bash
POST /api/admin/users/create/
Authorization: Token <admin-token>
Content-Type: application/json

{
  "username": "newuser",
  "password": "secure_password",
  "email": "user@example.com",
  "role": "staff"  // Options: staff, manager, admin
}
```

#### Delete User
```bash
DELETE /api/admin/users/<user_id>/delete/
Authorization: Token <admin-token>
```

**Note:** Requires admin role. Cannot delete your own account.

### CORS Configuration

The backend is configured with `CORS_ALLOW_ALL_ORIGINS = True` for development. **This should be changed in production** to specify allowed origins:

```python
# Production settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Development Notes

### Database
By default, the project uses SQLite. To use PostgreSQL or another database, set the `DATABASE_URL` environment variable.

### Signals
Stock movements automatically update item stock via Django signals:
- `receipt` → increases stock
- `issue` → decreases stock (prevents negative)
- `writeoff` → decreases stock (prevents negative)

### Validation
- Stock movements cannot result in negative stock for `issue` or `writeoff` types
- All quantities must be greater than 0
- Minimum stock levels must be non-negative

## Project Structure

```
kitchen-inventory/backend/
├── inventory/              # Main app
│   ├── models.py          # Item, StockMovement, Requisition models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # ViewSets and APIViews
│   ├── urls.py            # URL routing
│   ├── signals.py         # Stock update signals
│   ├── tests.py           # Test cases
│   └── management/
│       └── commands/
│           └── populate_sample_data.py
├── kitchen_inventory/     # Django project settings
│   ├── settings.py        # Django settings
│   └── urls.py            # Root URL config
├── manage.py
├── requirements.txt
└── README.md
```
