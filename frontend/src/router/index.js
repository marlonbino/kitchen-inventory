import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        title: 'Dashboard'
      }
    },
    {
      path: '/items',
      name: 'items',
      component: () => import('../views/ItemListView.vue'),
      meta: {
        title: 'Items'
      }
    },
    {
      path: '/movements',
      name: 'movements',
      component: () => import('../views/StockMovementHistoryView.vue'),
      meta: {
        title: 'Stock Movements'
      }
    },
    {
      path: '/requisitions',
      name: 'requisitions',
      component: () => import('../views/RequisitionManagerView.vue'),
      meta: {
        title: 'Requisitions'
      }
    },
    {
      path: '/low-stock',
      name: 'low-stock',
      component: () => import('../views/LowStockAlertView.vue'),
      meta: {
        title: 'Low Stock Alerts'
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

// Update document title on route change
router.beforeEach((to, from, next) => {
  document.title = to.meta.title 
    ? `${to.meta.title} - Kitchen Inventory System` 
    : 'Kitchen Inventory System'
  next()
})

export default router
