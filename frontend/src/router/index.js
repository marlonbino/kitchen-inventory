import { createRouter, createWebHistory } from 'vue-router'
import { getUserInfo } from '../services/api.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: 'Login'
      }
    },
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        title: 'Overview',
        requiresAuth: true
      }
    },
    {
      path: '/items',
      name: 'items',
      component: () => import('../views/ItemListView.vue'),
      meta: {
        title: 'Current Stock',
        requiresAuth: true
      }
    },
    {
      path: '/movements',
      name: 'movements',
      component: () => import('../views/StockMovementHistoryView.vue'),
      meta: {
        title: 'All Activities',
        requiresAuth: true
      }
    },
    {
      path: '/requisitions',
      name: 'requisitions',
      component: () => import('../views/RequisitionManagerView.vue'),
      meta: {
        title: 'Purchase Requests',
        requiresAuth: true
      }
    },
    {
      path: '/low-stock',
      name: 'low-stock',
      component: () => import('../views/LowStockAlertView.vue'),
      meta: {
        title: 'Running Low',
        requiresAuth: true
      }
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/CategoryManagementView.vue'),
      meta: {
        title: 'Manage Categories',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('../views/UserManagementView.vue'),
      meta: {
        title: 'Manage Users',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/AnalyticsView.vue'),
      meta: {
        title: 'Statistics',
        requiresAuth: true
      }
    },
    {
      path: '/in-transit',
      name: 'in-transit',
      component: () => import('../views/InTransitView.vue'),
      meta: {
        title: 'In Transit',
        requiresAuth: true
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: {
        title: 'Page Not Found'
      }
    }
  ]
})

// Navigation guard for authentication and title updates
router.beforeEach(async (to, from, next) => {
  // Update document title
  document.title = to.meta.title 
    ? `${to.meta.title} - BITZ Kitchen System` 
    : 'BITZ Kitchen System'
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    try {
      // Try to get user info to check if authenticated
      await getUserInfo()
      next()
    } catch (error) {
      // Not authenticated, redirect to login
      next({ name: 'login', query: { redirect: to.fullPath } })
    }
  } else {
    // Public route, allow access
    next()
  }
})

export default router
