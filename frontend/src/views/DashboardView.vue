<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <!-- Page Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-600 mt-1">Overview of your kitchen inventory</p>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="loading && !dashboardStats" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="n in 4" :key="n" class="bg-white rounded-lg shadow-md p-6 animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
            <div class="h-8 bg-gray-200 rounded w-3/4"></div>
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6 animate-pulse">
          <div class="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div class="space-y-3">
            <div v-for="n in 5" :key="n" class="h-16 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error && !loading" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <p class="text-red-800">Error loading dashboard: {{ error }}</p>
        </div>
        <button
          @click="loadDashboard"
          class="mt-3 text-sm text-red-700 hover:text-red-900 underline"
        >
          Try again
        </button>
      </div>

      <!-- Dashboard Content -->
      <div v-else class="space-y-6">
        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Total Items Card -->
          <BaseCard
            class="cursor-pointer hover:shadow-xl transition-shadow duration-200"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Total Items</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">
                  {{ dashboardStats?.total_items || 0 }}
                </p>
              </div>
              <div class="p-3 bg-blue-100 rounded-full">
                <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
            </div>
          </BaseCard>

          <!-- Low Stock Items Card -->
          <BaseCard
            class="cursor-pointer hover:shadow-xl transition-shadow duration-200"
            @click="navigateToLowStock"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Low Stock Items</p>
                <div class="flex items-center gap-2 mt-2">
                  <p class="text-3xl font-bold text-gray-900">
                    {{ dashboardStats?.low_stock_count || 0 }}
                  </p>
                  <span
                    v-if="(dashboardStats?.low_stock_count || 0) > 0"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
                  >
                    Alert
                  </span>
                </div>
              </div>
              <div class="p-3 bg-red-100 rounded-full">
                <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
            </div>
          </BaseCard>

          <!-- Pending Requisitions Card -->
          <BaseCard
            class="cursor-pointer hover:shadow-xl transition-shadow duration-200"
            @click="navigateToRequisitions"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Pending Requisitions</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">
                  {{ dashboardStats?.pending_requisitions || 0 }}
                </p>
              </div>
              <div class="p-3 bg-yellow-100 rounded-full">
                <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
          </BaseCard>

          <!-- Today's Movements Card -->
          <BaseCard class="hover:shadow-xl transition-shadow duration-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Today's Movements</p>
                <p class="text-3xl font-bold text-gray-900 mt-2">
                  {{ todayMovementsCount }}
                </p>
              </div>
              <div class="p-3 bg-green-100 rounded-full">
                <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                </svg>
              </div>
            </div>
          </BaseCard>
        </div>

        <!-- Low Stock Alert Section -->
        <BaseCard
          title="Low Stock Alerts"
          subtitle="Items requiring immediate attention"
        >
          <div v-if="lowStockItemsLoading" class="space-y-3">
            <div v-for="n in 5" :key="n" class="h-16 bg-gray-100 rounded animate-pulse"></div>
          </div>
          <div v-else-if="lowStockItems.length === 0" class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="mt-2 text-gray-500">No low stock items at the moment</p>
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="item in topLowStockItems"
              :key="item.id"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div class="flex-1">
                <div class="flex items-center gap-3">
                  <h4 class="font-semibold text-gray-900">{{ item.name }}</h4>
                  <span class="px-2 py-1 text-xs font-medium bg-gray-200 text-gray-700 rounded">
                    {{ item.category }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mt-1">{{ item.unit }}</p>
              </div>
              <StockBadge
                :current="item.current_stock"
                :minimum="item.min_stock_level"
                :show-percentage="false"
              />
            </div>
            <router-link
              v-if="lowStockItems.length > 5"
              to="/low-stock"
              class="block text-center text-blue-600 hover:text-blue-800 font-medium py-2"
            >
              View all {{ lowStockItems.length }} low stock items →
            </router-link>
          </div>
        </BaseCard>

        <!-- Recent Stock Movements Section -->
        <BaseCard
          title="Recent Stock Movements"
          subtitle="Last 10 stock movements"
        >
          <div v-if="movementsLoading" class="space-y-3">
            <div v-for="n in 10" :key="n" class="h-16 bg-gray-100 rounded animate-pulse"></div>
          </div>
          <div v-else-if="recentMovements.length === 0" class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p class="mt-2 text-gray-500">No stock movements yet</p>
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="movement in recentMovements"
              :key="movement.id"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center gap-4 flex-1">
                <!-- Movement Type Indicator -->
                <div
                  class="flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center"
                  :class="getMovementTypeColor(movement.movement_type)"
                >
                  <svg
                    v-if="movement.movement_type === 'receipt'"
                    class="w-6 h-6 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  <svg
                    v-else-if="movement.movement_type === 'issue'"
                    class="w-6 h-6 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                  </svg>
                  <svg
                    v-else
                    class="w-6 h-6 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>

                <!-- Movement Details -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <h4 class="font-semibold text-gray-900 truncate">
                      {{ movement.item_name || movement.item?.name || 'Unknown Item' }}
                    </h4>
                  </div>
                  <div class="flex items-center gap-3 mt-1">
                    <span class="text-sm text-gray-600">
                      {{ getMovementTypeLabel(movement.movement_type) }} • {{ movement.quantity }} {{ getItemUnit(movement) }}
                    </span>
                    <span class="text-xs text-gray-400">•</span>
                    <span class="text-xs text-gray-500">{{ formatRelativeTime(movement.date) }}</span>
                  </div>
                  <p v-if="movement.reference" class="text-xs text-gray-400 mt-1">
                    Ref: {{ movement.reference }}
                  </p>
                </div>
              </div>
            </div>
            <router-link
              v-if="recentMovements.length >= 10"
              to="/movements"
              class="block text-center text-blue-600 hover:text-blue-800 font-medium py-2"
            >
              View all movements →
            </router-link>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import BaseCard from '../components/BaseCard.vue'
import StockBadge from '../components/StockBadge.vue'

const router = useRouter()
const store = useInventoryStore()
const toast = useToast()

// Refs
const refreshInterval = ref(null)
const lowStockItemsLoading = ref(false)
const movementsLoading = ref(false)

// Computed properties
const loading = computed(() => store.loading.dashboardStats)
const error = computed(() => store.error.dashboardStats)
const dashboardStats = computed(() => store.dashboardStats)
const lowStockItems = computed(() => store.lowStockItems)
const recentMovements = computed(() => {
  // Prefer fetched movements (last 10), fallback to dashboard stats (last 5)
  if (store.stockMovements.length > 0) {
    return store.stockMovements.slice(0, 10)
  }
  if (dashboardStats.value?.recent_movements) {
    return dashboardStats.value.recent_movements
  }
  return []
})

const topLowStockItems = computed(() => {
  return lowStockItems.value.slice(0, 5)
})

const todayMovementsCount = computed(() => {
  if (!recentMovements.value.length) return 0
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  return recentMovements.value.filter(movement => {
    const movementDate = new Date(movement.date)
    movementDate.setHours(0, 0, 0, 0)
    return movementDate.getTime() === today.getTime()
  }).length
})

// Methods
const loadDashboard = async () => {
  try {
    await store.fetchDashboardStats()
    await loadLowStockItems()
    await loadRecentMovements()
  } catch (err) {
    toast.error('Failed to load dashboard data')
    console.error('Dashboard load error:', err)
  }
}

const loadLowStockItems = async () => {
  try {
    lowStockItemsLoading.value = true
    await store.fetchLowStock()
  } catch (err) {
    console.error('Low stock items load error:', err)
  } finally {
    lowStockItemsLoading.value = false
  }
}

const loadRecentMovements = async () => {
  try {
    movementsLoading.value = true
    await store.fetchStockMovements({ ordering: '-date' })
  } catch (err) {
    console.error('Recent movements load error:', err)
  } finally {
    movementsLoading.value = false
  }
}

const navigateToLowStock = () => {
  router.push('/low-stock')
}

const navigateToRequisitions = () => {
  router.push('/requisitions')
}

const formatRelativeTime = (dateString) => {
  if (!dateString) return 'Unknown'
  
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
  
  // Format date for older entries
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
  })
}

const getMovementTypeLabel = (type) => {
  const labels = {
    receipt: 'Receipt',
    issue: 'Issue',
    writeoff: 'Write-off'
  }
  return labels[type] || type
}

const getMovementTypeColor = (type) => {
  const colors = {
    receipt: 'bg-green-500',
    issue: 'bg-red-500',
    writeoff: 'bg-gray-500'
  }
  return colors[type] || 'bg-gray-500'
}

const getItemUnit = (movement) => {
  // Try to get unit from item data
  if (movement.item?.unit) return movement.item.unit
  // Fallback: try to get from items in store
  const item = store.itemById(movement.item_id)
  return item?.unit || 'units'
}

// Lifecycle
onMounted(() => {
  loadDashboard()
  
  // Set up auto-refresh every 30 seconds
  refreshInterval.value = setInterval(() => {
    loadDashboard()
  }, 30000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

