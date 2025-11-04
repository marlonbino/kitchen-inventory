# BITZ Kitchen Inventory Frontend

Modern Vue 3 + Vite frontend for the BITZ Kitchen Inventory Management System.

[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-blue.svg)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-4.0+-purple.svg)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0+-teal.svg)](https://tailwindcss.com/)

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Features](#-features)
- [Styling](#-styling)
- [Available Scripts](#-available-scripts)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🚀 Quick Start

### Prerequisites

- **Node.js 16+** and **npm 8+**
- Backend API running on `http://localhost:8000` (or configure via `.env`)

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at: **http://localhost:5173**

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend root directory:

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000/api
```

**Default Values:**
- If not set, defaults to `http://localhost:8000/api`

### Vite Configuration

See `vite.config.js` for build and development server settings:
- Port: `5173` (default)
- Proxy: Can be configured for API requests
- Build output: `dist/` directory

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── assets/                  # Static assets
│   │   ├── bitz-logo.svg        # BITZ logo (SVG)
│   │   └── bitz-logo-report.jpg # Logo for reports
│   ├── components/              # Reusable Vue components
│   │   ├── BaseButton.vue       # Button component
│   │   ├── BaseCard.vue         # Card container
│   │   ├── BaseModal.vue        # Modal dialog
│   │   ├── CategoryForm.vue     # Category management form
│   │   ├── ItemForm.vue         # Item create/edit form
│   │   ├── QuickStockForm.vue   # Quick stock actions
│   │   ├── Sidebar.vue          # Navigation sidebar
│   │   ├── StockMovementForm.vue # Stock movement form
│   │   └── TopHeader.vue        # App header
│   ├── composables/             # Vue composables
│   │   └── useDebounce.js       # Debounce utility
│   ├── router/                  # Vue Router
│   │   └── index.js             # Route definitions
│   ├── services/                # API service layer
│   │   └── api.js               # Axios API client
│   ├── stores/                  # Pinia state management
│   │   └── inventory.js         # Main inventory store
│   ├── views/                   # Page components
│   │   ├── AnalyticsView.vue    # Analytics & reports
│   │   ├── CategoryManagementView.vue # Category management
│   │   ├── DashboardView.vue    # Main dashboard
│   │   ├── InTransitView.vue    # Pending deliveries
│   │   ├── ItemListView.vue     # Inventory items list
│   │   ├── LoginView.vue        # Login page
│   │   ├── LowStockAlertView.vue # Low stock alerts
│   │   ├── RequisitionManagerView.vue # Purchase requests
│   │   ├── StockMovementHistoryView.vue # Stock movements
│   │   └── UserManagementView.vue # User admin (admin only)
│   ├── App.vue                  # Root component
│   ├── main.js                  # Application entry point
│   └── style.css                # Global styles
├── public/                      # Public assets
│   └── bitz-logo.svg
├── cypress/                     # E2E tests
│   ├── e2e/                     # Test specs
│   └── support/                 # Test utilities
├── index.html                   # HTML template
├── package.json                 # npm dependencies
├── tailwind.config.js           # Tailwind configuration
├── vite.config.js               # Vite configuration
└── README.md                    # This file
```

---

## 🏗️ Architecture

### State Management (Pinia)

The application uses **Pinia** for centralized state management:

**Main Store: `inventory.js`**
- User authentication state
- Inventory items
- Stock movements
- Purchase requests
- Low stock alerts
- Dashboard statistics
- Loading and error states

**Key Features:**
- Reactive state updates
- Computed getters
- Actions for async operations
- Persistent auth token

### API Service Layer

All API communication is handled through `src/services/api.js`:

**Features:**
- Axios-based HTTP client
- Centralized error handling
- Request/response interceptors
- Token-based authentication
- Automatic token attachment
- User-friendly error messages

**Main Functions:**
```javascript
// Authentication
login(username, password)
logout()
getCurrentUser()

// Items
getItems(params)
createItem(data)
updateItem(id, data)
deleteItem(id)

// Stock Movements
getStockMovements(params)
createStockMovement(data)

// Requisitions
getRequisitions(params)
createRequisition(data)
approveRequisition(id)
rejectRequisition(id)

// Admin
getUsers()
createUser(data)
deleteUser(id)

// Analytics
getDashboardStats()
getCategories()
```

### Component Architecture

**1. Base Components** (Reusable UI)
- `BaseButton.vue` - Customizable button
- `BaseCard.vue` - Card container with variants
- `BaseModal.vue` - Modal dialog

**2. Feature Components**
- `ItemForm.vue` - Item creation/editing
- `StockMovementForm.vue` - Stock transactions
- `QuickStockForm.vue` - Quick stock actions
- `CategoryForm.vue` - Category management
- `Sidebar.vue` - Navigation with badges
- `TopHeader.vue` - User info and dark mode

**3. Views** (Full Pages)
- Compose multiple components
- Handle data fetching
- Manage page-level state
- Implement business logic

### Router Configuration

**Routes:**
```javascript
/ (root)              → LoginView (if not authenticated)
                      → DashboardView (if authenticated)
/items                → ItemListView
/movements            → StockMovementHistoryView
/requisitions         → RequisitionManagerView
/low-stock            → LowStockAlertView
/in-transit           → InTransitView
/analytics            → AnalyticsView
/categories           → CategoryManagementView (admin only)
/users                → UserManagementView (admin only)
```

**Route Guards:**
- Authentication check on all routes (except login)
- Role-based access control for admin routes
- Automatic redirect to login if not authenticated

---

## 🎨 Styling

### Design System

**Framework:** Tailwind CSS 3.x

**Color Palette:**
- **Primary:** Blue (`blue-600`, `blue-700`)
- **Success:** Green (`green-600`, `green-700`)
- **Warning:** Yellow/Orange (`orange-600`, `yellow-600`)
- **Danger:** Red (`red-600`, `red-700`)
- **Neutral:** Gray (`gray-100` to `gray-900`)
- **Dark Mode:** Full dark mode support

**Typography:**
- **Font Family:** Roboto (via Google Fonts)
- **Headings:** Bold, various sizes
- **Body:** Regular weight
- **Monospace:** For numbers and codes

**Spacing:**
- Consistent spacing scale (0.25rem increments)
- Generous padding on cards and containers
- Balanced margins

### Dark Mode

**Implementation:**
- CSS class-based (`dark` class on `<html>`)
- Persistent preference (localStorage)
- Toggle in sidebar
- All components support dark mode
- Automatic color adjustments

**Key Classes:**
```css
bg-white dark:bg-neutral-800
text-gray-900 dark:text-white
border-gray-200 dark:border-neutral-700
```

### Responsive Design

**Approach:** Mobile-first

**Breakpoints:**
- `sm`: 640px (tablets)
- `md`: 768px (small laptops)
- `lg`: 1024px (desktops)
- `xl`: 1280px (large screens)

**Responsive Features:**
- Sidebar collapses to hamburger on mobile
- Tables become scrollable or cards on small screens
- Stacked layouts on mobile, grid on desktop
- Touch-friendly button sizes

### Card Design

**Modern Gradient Cards:**
- Gradient backgrounds for visual hierarchy
- Hover effects with scale transform
- Consistent border radius (12px)
- Box shadows for depth
- Icon badges with gradients

---

## ✨ Features

### 1. User Authentication
- 🔐 Token-based authentication
- 👤 User profile with role display
- 🚪 Secure logout
- 🔒 Auto-logout on token expiration
- 🛡️ Role-based access control

### 2. Dashboard
- 📊 Key metrics (Total Items, Low Stock, Pending Requests, Total Value)
- ⚠️ Low stock items table
- 📈 Recent activity timeline
- 🔄 Real-time updates
- 🎨 Beautiful gradient cards

### 3. Inventory Management
- ➕ Add new items
- ✏️ Edit existing items
- 🗑️ Delete items
- 🔍 Search and filter
- 📂 Category filtering
- 📊 Stock level indicators
- 💰 Price tracking
- 🏭 Supplier information

### 4. Stock Movements
- 📥 **Receive Stock** - Record incoming deliveries
- 📤 **Track Usage** - Record consumption
- 🗑️ **Record Waste** - Log damaged/expired items
- 🕒 Complete transaction history
- 👤 User attribution
- 📝 Notes for each movement
- 🔍 Filter by type, date, item

### 5. Purchase Requests (Requisitions)
- 📋 Create purchase requests
- ✅ Approve/reject workflow
- 🚚 Assign deliveries
- ✔️ Confirm deliveries
- 📊 Status tracking (Pending, Approved, Awaiting Delivery, Received)
- 📝 Justification notes
- 🔔 Badge notifications for pending approvals

### 6. Low Stock Alerts
- ⚠️ Real-time low stock monitoring
- 🎨 Color-coded urgency (red = critical, yellow = low)
- 🔢 Stock percentage display
- 🛒 Quick purchase request creation
- 📥 Quick stock receipt
- 📊 Category breakdown

### 7. Analytics & Reports
- 📈 Dashboard statistics
- 📊 Items by category chart
- 🔥 Most used items
- 📅 Recent activity
- 📄 **Printable Reports** with BITZ branding
  - Customizable date ranges
  - Professional PDF output
  - Summary statistics
  - Low stock alerts section
  - Category breakdown

### 8. User Management (Admin Only)
- 👥 View all users
- ➕ Create new users
- 🗑️ Delete users
- 👤 Assign roles (Staff, Manager, Admin)
- 🎨 Role-based color coding
- 🛡️ Self-deletion prevention

### 9. Category Management (Admin Only)
- 📂 Create categories
- ✏️ Edit categories
- 🗑️ Delete categories
- 🎨 Visual category cards
- 📊 Item count per category

### User Experience Features

- 🔔 **Toast Notifications** - Instant feedback for all actions
- ⏳ **Loading States** - Skeleton loaders and spinners
- ❌ **Error Handling** - User-friendly error messages
- ✅ **Confirmation Dialogs** - For destructive actions
- ⌨️ **Keyboard Support** - ESC to close modals
- 🎯 **Auto-focus** - In modals and forms
- 🔍 **Debounced Search** - Optimized search performance
- 📱 **Responsive** - Works on all device sizes
- 🌓 **Dark Mode** - Full theme support

---

## 📦 Available Scripts

```bash
# Development
npm run dev          # Start dev server with hot reload (http://localhost:5173)

# Production
npm run build        # Build for production (output: dist/)
npm run preview      # Preview production build

# Testing
npx cypress open     # Open Cypress Test Runner (interactive)
npx cypress run      # Run Cypress tests (headless)

# Utilities
npm run lint         # Run ESLint (if configured)
npm run format       # Format code with Prettier (if configured)
```

### Development Server

```bash
npm run dev
```
- Hot Module Replacement (HMR)
- Fast refresh for Vue components
- Available at `http://localhost:5173`
- Automatically opens in browser

### Production Build

```bash
npm run build
```
- Minified and optimized output
- Tree-shaking for smaller bundles
- Static assets with cache-busting hashes
- Output in `dist/` directory
- Ready for deployment

---

## 🧪 Testing

### Cypress E2E Tests

**Test Coverage:**
- ✅ User authentication (login/logout)
- ✅ Dashboard functionality
- ✅ Inventory management (CRUD operations)
- ✅ Stock movements (receive, usage, waste)
- ✅ Purchase requests (create, approve, reject, confirm)
- ✅ Low stock alerts
- ✅ Analytics and report generation
- ✅ User management (admin)
- ✅ Category management (admin)
- ✅ Dark mode toggle
- ✅ Navigation and routing

**Running Tests:**

1. **Ensure backend and frontend are running:**
```bash
# Terminal 1: Backend
cd backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm run dev
```

2. **Run Cypress:**
```bash
# Terminal 3: In frontend directory
# Interactive mode (recommended for development)
npx cypress open

# Headless mode (for CI/CD)
npx cypress run
```

**Test Files Location:**
```
frontend/cypress/e2e/
├── auth.cy.js           # Authentication tests
├── dashboard.cy.js      # Dashboard tests
├── inventory.cy.js      # Inventory CRUD tests
├── movements.cy.js      # Stock movements tests
├── requisitions.cy.js   # Purchase requests tests
└── admin.cy.js          # Admin functionality tests
```

### Manual Testing Checklist

**Authentication:**
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Logout functionality
- [ ] Token persistence
- [ ] Auto-redirect when not authenticated

**Inventory:**
- [ ] View inventory list
- [ ] Search items
- [ ] Filter by category
- [ ] Create new item
- [ ] Edit item
- [ ] Delete item
- [ ] Quick stock actions

**Stock Movements:**
- [ ] Receive stock
- [ ] Track usage
- [ ] Record waste
- [ ] View movement history
- [ ] Filter movements

**Purchase Requests:**
- [ ] Create requisition
- [ ] View requisitions list
- [ ] Approve requisition (manager/admin)
- [ ] Reject requisition (manager/admin)
- [ ] Assign delivery (manager/admin)
- [ ] Confirm delivery

**Low Stock:**
- [ ] View low stock alerts
- [ ] Create requisition from alert
- [ ] Quick receive stock

**Analytics:**
- [ ] View dashboard stats
- [ ] Generate report
- [ ] Print report

**Admin Functions:**
- [ ] Create user
- [ ] Delete user
- [ ] Create category
- [ ] Edit category
- [ ] Delete category

**UI/UX:**
- [ ] Dark mode toggle
- [ ] Responsive on mobile
- [ ] Toast notifications
- [ ] Loading states
- [ ] Error handling

---

## 🐛 Troubleshooting

### Common Issues

#### **1. API Connection Errors**

**Problem:** Cannot connect to backend API

**Solutions:**
- Verify backend is running: `http://localhost:8000`
- Check `.env` file has correct `VITE_API_BASE_URL`
- Verify CORS is properly configured in Django settings
- Check browser console for detailed errors

#### **2. Build Errors**

**Problem:** `npm run build` fails

**Solutions:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite

# Update dependencies
npm update
```

#### **3. Authentication Issues**

**Problem:** Login not working or token errors

**Solutions:**
- Check localStorage for `auth_token`
- Verify backend authentication endpoint is working
- Clear browser cache and localStorage
- Check network tab in DevTools for API responses

#### **4. Styling Issues**

**Problem:** Tailwind classes not working

**Solutions:**
- Verify `tailwind.config.js` is correct
- Check `postcss.config.js` exists
- Restart dev server after config changes
- Clear browser cache

#### **5. Routing Issues**

**Problem:** 404 errors or wrong redirects

**Solutions:**
- Check route definitions in `src/router/index.js`
- Verify route guards are working
- Check for typos in `router-link` paths
- Clear browser history and cache

#### **6. Dark Mode Not Working**

**Problem:** Dark mode toggle doesn't work

**Solutions:**
- Check `<html>` element has `dark` class
- Verify localStorage has `theme` key
- Check all components use dark mode classes
- Restart browser

#### **7. Report Generation Issues**

**Problem:** Report doesn't print or shows blank

**Solutions:**
- Allow pop-ups in browser
- Check browser console for errors
- Verify BITZ logo is loading correctly
- Try different browser
- Check print CSS media queries

### Getting Help

1. **Check Browser Console:** Look for JavaScript errors
2. **Check Network Tab:** Verify API requests/responses
3. **Review Logs:** Check backend logs for errors
4. **Search Issues:** Check GitHub issues for similar problems
5. **Contact Support:** Email support@bitz-it.com

### Debugging Tips

```bash
# Enable verbose logging
VITE_LOG_LEVEL=debug npm run dev

# Check Vite config
cat vite.config.js

# Verify Node/npm versions
node --version
npm --version

# Test API connectivity
curl http://localhost:8000/api/

# Clear all caches
rm -rf node_modules/.vite
rm -rf dist
npm cache clean --force
```

---

## 🔄 Integration with Backend

The frontend communicates with the Django REST Framework backend:

**API Base URL:** `http://localhost:8000/api`

**Authentication:**
- Token-based (Django REST Framework tokens)
- Token stored in localStorage
- Automatically attached to all requests via Axios interceptors

**Key Endpoints Used:**
```
POST   /api/auth/login/                    # User login
POST   /api/auth/logout/                   # User logout
GET    /api/auth/user/                     # Get current user

GET    /api/items/                         # List items
POST   /api/items/                         # Create item
GET    /api/items/{id}/                    # Get item
PUT    /api/items/{id}/                    # Update item
DELETE /api/items/{id}/                    # Delete item

GET    /api/categories/                    # List categories
POST   /api/categories/                    # Create category

GET    /api/stock-movements/               # List movements
POST   /api/stock-movements/               # Create movement

GET    /api/requisitions/                  # List requisitions
POST   /api/requisitions/                  # Create requisition
POST   /api/requisitions/{id}/approve/     # Approve
POST   /api/requisitions/{id}/reject/      # Reject
POST   /api/requisitions/{id}/assign/      # Assign delivery
POST   /api/requisitions/{id}/confirm/     # Confirm delivery

GET    /api/low-stock/                     # Get low stock items
GET    /api/dashboard-stats/               # Get dashboard stats

GET    /api/admin/users/                   # List users (admin)
POST   /api/admin/users/create/            # Create user (admin)
DELETE /api/admin/users/{id}/delete/       # Delete user (admin)
```

**Error Handling:**
- API errors are caught and displayed as toast notifications
- Network errors show user-friendly messages
- 401 errors trigger automatic logout and redirect to login

---

## 📝 Code Style

### Vue 3 Composition API

- Use `<script setup>` syntax
- Prefer `ref` and `reactive` for state
- Use computed properties for derived state
- Use `onMounted` for lifecycle hooks

**Example:**
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const items = ref([])
const loading = ref(false)

const totalItems = computed(() => items.value.length)

onMounted(async () => {
  loading.value = true
  items.value = await fetchItems()
  loading.value = false
})
</script>
```

### JavaScript

- ES6+ syntax (arrow functions, destructuring, etc.)
- Async/await for asynchronous operations
- Proper error handling with try/catch
- JSDoc comments for complex functions

### Tailwind CSS

- Utility-first approach
- Use Tailwind classes instead of custom CSS
- Dark mode support: `dark:` prefix
- Responsive: `sm:`, `md:`, `lg:` prefixes

**Example:**
```html
<div class="bg-white dark:bg-neutral-800 rounded-lg shadow-md p-6">
  <h2 class="text-xl font-bold text-gray-900 dark:text-white">
    Title
  </h2>
</div>
```

---

## 🤝 Contributing

### Development Guidelines

1. **Follow Vue 3 Best Practices**
   - Use Composition API with `<script setup>`
   - Keep components small and focused
   - Extract reusable logic into composables

2. **Component Design**
   - Props for configuration
   - Emits for communication
   - Slots for flexibility
   - Proper prop validation

3. **State Management**
   - Use Pinia for global state
   - Keep component state local when possible
   - Actions for side effects

4. **Styling**
   - Use Tailwind CSS utilities
   - Support dark mode
   - Make it responsive
   - Follow design system

5. **Error Handling**
   - Catch all errors
   - Show user-friendly messages
   - Log errors to console (development)
   - Handle edge cases

6. **Testing**
   - Write Cypress tests for new features
   - Test happy paths and edge cases
   - Ensure tests are reliable

7. **Code Quality**
   - Use meaningful variable names
   - Add comments for complex logic
   - Keep functions small and focused
   - Remove console.logs before committing

### Pull Request Process

1. Create feature branch from `develop`
2. Make changes and test thoroughly
3. Update documentation if needed
4. Submit PR with clear description
5. Wait for code review
6. Address feedback
7. Merge after approval

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

### Resources
- 📘 [User Manual](../USER_MANUAL.md)
- 📗 [Backend README](../backend/README.md)
- 📙 [Main README](../README.md)

---

**Made with ❤️ by BITZ IT Consulting LTD**
