# Kitchen Inventory Frontend

Vue 3 + Vite frontend application for kitchen inventory management system.

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000` (or configure `VITE_API_BASE_URL`)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── BaseButton.vue
│   ├── BaseCard.vue
│   ├── BaseInput.vue
│   ├── BaseModal.vue
│   ├── BaseSelect.vue
│   ├── ConfirmDialog.vue
│   ├── EmptyState.vue
│   ├── ItemForm.vue
│   ├── LoadingSpinner.vue
│   ├── NavBar.vue
│   ├── QuickStockForm.vue
│   ├── RequisitionForm.vue
│   ├── StockBadge.vue
│   └── StockMovementForm.vue
├── composables/        # Vue composables
│   └── useDebounce.js
├── router/            # Vue Router configuration
│   └── index.js
├── services/          # API service layer
│   └── api.js
├── stores/            # Pinia state management
│   └── inventory.js
├── utils/             # Utility functions
│   └── debounce.js
├── views/             # Page components
│   ├── DashboardView.vue
│   ├── ItemListView.vue
│   ├── LowStockAlertView.vue
│   ├── NotFoundView.vue
│   ├── RequisitionManagerView.vue
│   └── StockMovementHistoryView.vue
├── App.vue            # Root component
├── main.js            # Application entry point
└── style.css          # Global styles (Tailwind CSS)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend root:

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000/api
```

### Tailwind CSS

The project uses Tailwind CSS for styling. Configuration is in `tailwind.config.js`.

### Router

Routes are configured in `src/router/index.js`:
- `/` - Dashboard
- `/items` - Item Management
- `/movements` - Stock Movement History
- `/requisitions` - Requisition Manager
- `/low-stock` - Low Stock Alerts

## 🏗️ Architecture

### State Management (Pinia)

The application uses Pinia for state management with a single store (`inventory.js`) that manages:
- Items
- Stock Movements
- Requisitions
- Low Stock Items
- Dashboard Statistics
- Loading states
- Error states

### API Service Layer

All API calls are handled through `src/services/api.js` using Axios:
- Centralized error handling
- Request/response interceptors
- Retry logic for failed requests
- User-friendly error messages

### Component Architecture

- **Base Components**: Reusable UI components (Button, Card, Input, etc.)
- **Feature Components**: Components specific to features (ItemForm, StockMovementForm, etc.)
- **Views**: Full page components that compose multiple components

## 🎨 Styling

### Color Scheme

- **Primary**: Blue-600
- **Success**: Green-600
- **Warning**: Yellow-500
- **Danger**: Red-600

### Responsive Design

- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Tables become cards on mobile
- Hamburger menu for navigation on mobile

## 🔑 Features

### Core Functionality

1. **Item Management**
   - CRUD operations for inventory items
   - Category and unit management
   - Stock level tracking
   - Quick stock movements (issue/receipt)

2. **Stock Movements**
   - Record receipts, issues, and write-offs
   - Filter by type, item, date range
   - Pagination support
   - CSV export
   - Running stock balance calculation

3. **Requisitions**
   - Create requisition requests
   - Approve/reject with confirmation
   - Bulk approve functionality
   - Status tracking (pending/approved/rejected)

4. **Low Stock Alerts**
   - Visual indicators for low stock items
   - Color-coded priority levels
   - Quick actions (create requisition, quick receipt)
   - Batch requisition creation
   - Auto-refresh every 60 seconds

5. **Dashboard**
   - Overview statistics
   - Low stock alerts section
   - Recent stock movements
   - Auto-refresh every 30 seconds

### User Experience Features

- **Toast Notifications**: Success/error feedback for all actions
- **Loading States**: Skeleton loaders and spinners
- **Error Handling**: User-friendly error messages
- **Confirmation Dialogs**: For destructive actions
- **Keyboard Shortcuts**: ESC to close modals
- **Focus Management**: Auto-focus in modals
- **Debounced Search**: Optimized search input
- **Responsive Tables**: Convert to cards on mobile

## 📦 Available Scripts

```bash
# Development
npm run dev          # Start dev server with hot reload

# Production
npm run build        # Build for production
npm run preview      # Preview production build

# Linting (if configured)
npm run lint          # Run linter
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Create a new item
- [ ] Edit an existing item
- [ ] Delete an item (with confirmation)
- [ ] Record stock movement (receipt)
- [ ] Record stock movement (issue)
- [ ] Record stock movement (write-off)
- [ ] Verify stock updates automatically
- [ ] Create a requisition
- [ ] Approve a requisition
- [ ] Reject a requisition
- [ ] Bulk approve requisitions
- [ ] Check low stock alerts appear correctly
- [ ] Test all filters and search
- [ ] Test pagination
- [ ] Test CSV exports
- [ ] Verify dashboard stats are accurate
- [ ] Test responsive design on mobile/tablet

## 🐛 Troubleshooting

### Common Issues

**API Connection Errors**
- Verify backend is running on the configured port
- Check `VITE_API_BASE_URL` in `.env`
- Check CORS configuration in backend

**Build Errors**
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

**Routing Issues**
- Ensure all routes are defined in `src/router/index.js`
- Check route paths match navigation links

## 🔄 Integration with Backend

The frontend communicates with the Django REST Framework backend:
- Base URL: `http://localhost:8000/api` (configurable)
- All API endpoints follow RESTful conventions
- Stock movements automatically update item stock via Django signals
- Real-time updates through periodic data fetching

## 📝 Code Style

- Vue 3 Composition API with `<script setup>`
- ES6+ JavaScript
- Tailwind CSS for styling
- ESLint/Prettier (if configured)

## 🤝 Contributing

1. Follow Vue 3 best practices
2. Use Composition API with `<script setup>`
3. Keep components small and focused
4. Add proper error handling
5. Include loading states
6. Make components responsive
7. Add proper TypeScript/JSDoc comments

## 📄 License

See project root LICENSE file.
