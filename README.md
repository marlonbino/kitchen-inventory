# BITZ Kitchen Inventory Management System

<div align="center">

![BITZ Logo](frontend/public/bitz-logo.svg)

**A comprehensive kitchen inventory management system for BITZ IT Consulting LTD**

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-blue.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Support](#support)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [User Roles](#user-roles)
- [Documentation](#documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The BITZ Kitchen Inventory Management System is a full-stack web application designed to streamline kitchen inventory operations, track stock movements, manage purchase requests, and generate insightful reports. Built with modern technologies and best practices, it offers an intuitive interface with role-based access control.

### Key Highlights

- 🔒 **Secure** - Role-based access control with admin-only user management
- 📱 **Responsive** - Works seamlessly on desktop, tablet, and mobile devices
- 🌓 **Dark Mode** - Eye-friendly interface with theme switching
- 📊 **Analytics** - Comprehensive reporting and data visualization
- ⚡ **Real-time** - Instant updates and live stock tracking
- 🎨 **Modern UI** - Beautiful gradients and intuitive design

---

## ✨ Features

### Inventory Management
- ✅ Add, edit, and delete inventory items
- ✅ Track stock levels in real-time
- ✅ Categorize items for easy organization
- ✅ Set minimum stock levels for alerts
- ✅ Record prices and supplier information

### Stock Movements
- ✅ Track stock receipts (incoming stock)
- ✅ Record usage (consumption in kitchen)
- ✅ Log waste and spillage
- ✅ Complete movement history with timestamps
- ✅ User attribution for all transactions

### Purchase Requests (Requisitions)
- ✅ Create purchase requests for items
- ✅ Approval workflow (Pending → Approved → Received)
- ✅ Assign deliveries to staff
- ✅ Confirm received deliveries
- ✅ Track request status

### Alerts & Notifications
- ✅ Low stock alerts dashboard
- ✅ Critical stock warnings (0 quantity)
- ✅ Real-time badge notifications
- ✅ Color-coded urgency indicators

### Analytics & Reports
- ✅ Dashboard with key metrics
- ✅ Items by category breakdown
- ✅ Most used items tracking
- ✅ Recent activity timeline
- ✅ Printable PDF reports with BITZ branding

### User Management (Admin Only)
- ✅ Create user accounts
- ✅ Assign roles (Staff, Manager, Admin)
- ✅ View all system users
- ✅ Delete users (with self-deletion prevention)
- ✅ Role-based color coding

### Category Management (Admin Only)
- ✅ Create custom categories
- ✅ Edit category details
- ✅ Delete unused categories
- ✅ Visual category cards

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 4.2+
- **API:** Django REST Framework 3.14+
- **Authentication:** Token Authentication
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **CORS:** django-cors-headers
- **Environment:** python-decouple

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Build Tool:** Vite 4+
- **Routing:** Vue Router 4
- **State Management:** Pinia
- **Styling:** Tailwind CSS 3
- **HTTP Client:** Axios
- **Notifications:** Vue Toastification
- **Icons:** Heroicons (inline SVG)

### Development Tools
- **Testing:** Cypress (E2E)
- **Version Control:** Git
- **Package Managers:** npm, pip

---

## 📁 Project Structure

```
kitchen-inventory/
├── backend/                      # Django Backend
│   ├── inventory/                # Main app
│   │   ├── migrations/           # Database migrations
│   │   ├── management/           # Custom commands
│   │   │   └── commands/
│   │   │       ├── seed_test_data.py
│   │   │       └── change_admin_password.py
│   │   ├── admin.py              # Django admin config
│   │   ├── auth_views.py         # Authentication endpoints
│   │   ├── models.py             # Database models
│   │   ├── serializers.py        # DRF serializers
│   │   ├── views.py              # API views
│   │   ├── urls.py               # URL routing
│   │   └── signals.py            # Django signals
│   ├── kitchen_inventory/        # Project settings
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Root URLs
│   │   └── wsgi.py               # WSGI config
│   ├── manage.py                 # Django management
│   ├── requirements.txt          # Python dependencies
│   ├── change_admin_password.py  # Password reset script
│   └── README.md                 # Backend documentation
│
├── frontend/                     # Vue Frontend
│   ├── src/
│   │   ├── assets/               # Images and static files
│   │   │   ├── bitz-logo.svg
│   │   │   └── bitz-logo-report.jpg
│   │   ├── components/           # Vue components
│   │   │   ├── BaseButton.vue
│   │   │   ├── BaseCard.vue
│   │   │   ├── BaseModal.vue
│   │   │   ├── CategoryForm.vue
│   │   │   ├── ItemForm.vue
│   │   │   ├── QuickStockForm.vue
│   │   │   ├── Sidebar.vue
│   │   │   ├── StockMovementForm.vue
│   │   │   └── TopHeader.vue
│   │   ├── views/                # Page components
│   │   │   ├── AnalyticsView.vue
│   │   │   ├── CategoryManagementView.vue
│   │   │   ├── DashboardView.vue
│   │   │   ├── InTransitView.vue
│   │   │   ├── ItemListView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── LowStockAlertView.vue
│   │   │   ├── RequisitionManagerView.vue
│   │   │   ├── StockMovementHistoryView.vue
│   │   │   └── UserManagementView.vue
│   │   ├── router/               # Vue Router
│   │   ├── stores/               # Pinia stores
│   │   ├── services/             # API services
│   │   ├── composables/          # Vue composables
│   │   ├── App.vue               # Root component
│   │   └── main.js               # Entry point
│   ├── public/                   # Static assets
│   ├── cypress/                  # E2E tests
│   ├── index.html                # HTML template
│   ├── package.json              # npm dependencies
│   ├── tailwind.config.js        # Tailwind config
│   ├── vite.config.js            # Vite config
│   └── README.md                 # Frontend documentation
│
├── .gitignore                    # Git ignore rules
├── USER_MANUAL.md                # End-user documentation
└── README.md                     # This file
```

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

### Required Software
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **npm 8+** - (comes with Node.js)
- **Git** - [Download](https://git-scm.com/)

### Verify Installation

```bash
# Check Python version
python --version  # Should be 3.9+

# Check Node.js version
node --version    # Should be 16+

# Check npm version
npm --version     # Should be 8+

# Check Git version
git --version
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/BITZ-IT-Consulting-LTD/inventory-system.git
cd inventory-system
```

### 2. Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create sample data (optional)
python manage.py seed_test_data

# Start backend server
python manage.py runserver
```

Backend will run at: **http://localhost:8000**

### 3. Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: **http://localhost:5173**

### 4. Access the System

Open your browser and navigate to: **http://localhost:5173**

**Default Login Credentials:**
- Username: `admin`
- Password: `p@ssw0rd`

> 🔒 **Security:** Change the default password immediately after first login!

---

## 📖 Detailed Setup

### Backend Setup (Detailed)

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

#### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- Django 4.2+
- djangorestframework
- django-cors-headers
- python-decouple
- Pillow (for image handling)

#### 4. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Seed test data (recommended for development)
python manage.py seed_test_data
```

#### 5. Change Admin Password

```bash
# Using the script
python change_admin_password.py

# Or using Django shell
python manage.py shell
```

Then in shell:
```python
from django.contrib.auth.models import User
admin = User.objects.get(username='admin')
admin.set_password('your_new_password')
admin.save()
exit()
```

#### 6. Run Backend Server

```bash
python manage.py runserver
```

Or specify port:
```bash
python manage.py runserver 8000
```

**API will be available at:**
- Main: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

### Frontend Setup (Detailed)

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Environment Configuration (Optional)

Create `.env` file in frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

#### 3. Run Development Server

```bash
npm run dev
```

**Available Scripts:**
```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
npm run test     # Run Cypress tests
```

#### 4. Build for Production

```bash
npm run build
```

Build output will be in `frontend/dist/`

---

## 👥 User Roles

The system has three user roles with different permission levels:

### 🟢 Kitchen Staff
**Permissions:**
- ✅ View inventory items
- ✅ Create purchase requests
- ✅ Record stock movements (usage, receipt, waste)
- ✅ View low stock alerts
- ✅ Access basic analytics
- ❌ Cannot approve requests
- ❌ Cannot manage users or categories

### 🔵 Manager
**Permissions:**
- ✅ All Kitchen Staff permissions
- ✅ Approve/reject purchase requests
- ✅ Assign deliveries
- ✅ Add/edit/delete inventory items
- ✅ Access detailed analytics and reports
- ❌ Cannot manage users or categories

### 🟣 Administrator
**Permissions:**
- ✅ All Manager permissions
- ✅ Create and delete user accounts
- ✅ Manage categories
- ✅ Full system access
- ✅ Advanced configuration

---

## 📚 Documentation

### For End Users
📘 **[User Manual](USER_MANUAL.md)** - Comprehensive guide for using the system

### For Developers
- 📗 **[Backend README](backend/README.md)** - Backend setup and API documentation
- 📙 **[Frontend README](frontend/README.md)** - Frontend development guide

### API Documentation
Access the browsable API at: **http://localhost:8000/api/**

**Main Endpoints:**
```
/api/auth/login/                  - User login
/api/auth/logout/                 - User logout
/api/auth/user/                   - Get current user info
/api/items/                       - Inventory items CRUD
/api/categories/                  - Categories CRUD
/api/stock-movements/             - Stock movements CRUD
/api/requisitions/                - Requisitions CRUD
/api/low-stock/                   - Low stock items
/api/dashboard-stats/             - Dashboard statistics
/api/admin/users/                 - User management (admin only)
/api/admin/users/create/          - Create user (admin only)
/api/admin/users/<id>/delete/     - Delete user (admin only)
```

---

## 🧪 Testing

### Running Cypress Tests

#### 1. Ensure both backend and frontend are running

```bash
# Terminal 1: Backend
cd backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev
```

#### 2. Run Cypress Tests

```bash
# Terminal 3: In frontend directory
cd frontend

# Open Cypress Test Runner (Interactive)
npx cypress open

# Run tests headlessly
npx cypress run
```

### Test Coverage

The test suite covers:
- ✅ User authentication
- ✅ Dashboard functionality
- ✅ Inventory management (CRUD)
- ✅ Stock movements
- ✅ Purchase requests workflow
- ✅ Low stock alerts
- ✅ Analytics and reporting
- ✅ User management (admin)
- ✅ Category management (admin)

---

## 🚀 Deployment

### Production Checklist

#### Backend
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up proper `ALLOWED_HOSTS`
- [ ] Configure static files serving
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set up backup system
- [ ] Configure email backend
- [ ] Set up monitoring

#### Frontend
- [ ] Build for production (`npm run build`)
- [ ] Configure proper API URL
- [ ] Enable service worker (PWA)
- [ ] Optimize assets
- [ ] Set up CDN (optional)
- [ ] Configure caching
- [ ] Enable compression

### Deployment Options

#### Option 1: Traditional Server
1. Deploy Django with Gunicorn/uWSGI
2. Use Nginx as reverse proxy
3. Serve static files via Nginx
4. Set up SSL with Let's Encrypt

#### Option 2: Platform as a Service
- **Backend:** Heroku, Railway, Render
- **Frontend:** Vercel, Netlify, AWS Amplify
- **Database:** Railway, ElephantSQL, AWS RDS

#### Option 3: Docker
Use Docker containers for easy deployment:

```bash
# Build Docker images
docker-compose build

# Run containers
docker-compose up -d
```

---

## 🔧 Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Error: Module not found
pip install -r requirements.txt

# Error: Database locked
python manage.py migrate --run-syncdb

# Error: Port in use
python manage.py runserver 8001  # Use different port
```

#### Frontend won't start
```bash
# Error: Module not found
rm -rf node_modules package-lock.json
npm install

# Error: Port in use
# Edit vite.config.js and change port

# Error: API connection failed
# Check VITE_API_BASE_URL in .env
```

#### Cannot log in
```bash
# Reset admin password
cd backend
python change_admin_password.py

# Or create new superuser
python manage.py createsuperuser
```

#### CORS errors
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in backend settings
- Verify frontend URL is in allowed origins

### Getting Help

1. Check the [User Manual](USER_MANUAL.md)
2. Review backend/frontend READMEs
3. Search existing issues on GitHub
4. Contact technical support: support@bitz-it.com

---

## 🤝 Contributing

### Branching Strategy

- `main/master` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Production hotfixes

### Workflow

1. Create feature branch from `develop`
2. Make changes and commit
3. Push branch to repository
4. Create Pull Request to `develop`
5. Wait for code review and approval
6. Merge after approval

### Code Standards

- **Python:** Follow PEP 8
- **JavaScript:** Follow ESLint rules
- **Vue:** Follow Vue.js style guide
- **Git Commits:** Use conventional commits

---

## 📄 License

**Proprietary Software**

© 2025 BITZ IT Consulting LTD. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

## 📞 Support

### Technical Support
- **Email:** support@bitz-it.com
- **Hours:** Monday-Friday, 8 AM - 6 PM EAT

### System Administrator
Contact your organization's IT department for:
- User account issues
- Permission requests
- System access
- Training

---

## 🙏 Acknowledgments

- **BITZ IT Consulting LTD** - System development and maintenance
- **Django** & **Django REST Framework** - Backend framework
- **Vue.js** - Frontend framework
- **Tailwind CSS** - UI styling
- All contributors and testers

---

## 📊 System Statistics

- **Version:** 2.0
- **Release Date:** November 2025
- **Lines of Code:** 10,000+
- **Components:** 20+
- **API Endpoints:** 15+
- **Database Tables:** 7
- **Supported Languages:** English

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Email notifications
- [ ] Barcode scanning
- [ ] Mobile apps (iOS/Android)
- [ ] Batch import/export
- [ ] Recipe management
- [ ] Supplier management
- [ ] Purchase order generation

---

<div align="center">

**Made with ❤️ by BITZ IT Consulting LTD**

[Documentation](USER_MANUAL.md) • [Report Bug](https://github.com/BITZ-IT-Consulting-LTD/inventory-system/issues) • [Request Feature](https://github.com/BITZ-IT-Consulting-LTD/inventory-system/issues)

</div>

