<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-3 sm:p-4 md:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Page Header -->
      <div class="mb-6">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Running Low</h1>
        <p class="text-gray-600 dark:text-gray-300 mt-1">
          {{ summaryText }}
        </p>
      </div>

      <!-- Critical Alert Banner -->
      <div
        v-if="criticalItems.length > 0"
        class="mb-6 p-4 bg-red-100 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-400 rounded-r-lg animate-pulse"
      >
        <div class="flex items-center">
          <svg class="w-6 h-6 text-red-600 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-red-800 dark:text-red-400">
              Critical Alert: {{ criticalItems.length }} item(s) are out of stock!
            </h3>
            <p class="text-sm text-red-700 dark:text-red-300 mt-1">
              Immediate action required. These items need urgent restocking.
            </p>
          </div>
        </div>
      </div>

      <!-- Quick Actions Bar -->
      <div class="mb-6 flex flex-wrap gap-3">
        <BaseButton
          v-if="filteredItems.length > 0"
          variant="primary"
          @click="showBatchRequisitionModal = true"
          :disabled="loading || batchActionLoading"
        >
          <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Create Requisitions for All ({{ filteredItems.length }})
        </BaseButton>
        <BaseButton
          variant="secondary"
          @click="exportToCSV"
          :disabled="loading || filteredItems.length === 0"
        >
          <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Export Report
        </BaseButton>
      </div>

      <!-- Filters and Sort -->
      <BaseCard class="mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Search -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Search</label>
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by item name..."
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-neutral-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 bg-white dark:bg-neutral-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
              />
              <svg
                class="absolute left-3 top-2.5 h-5 w-5 text-gray-400 dark:text-gray-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          <!-- Category Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Category</label>
            <select
              v-model="selectedCategory"
              class="block w-full px-3 py-2 border border-gray-300 dark:border-neutral-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 bg-white dark:bg-neutral-800 text-gray-900 dark:text-white"
            >
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <!-- Sort -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Sort By</label>
            <select
              v-model="sortBy"
              class="block w-full px-3 py-2 border border-gray-300 dark:border-neutral-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 bg-white dark:bg-neutral-800 text-gray-900 dark:text-white"
            >
              <option value="critical">Most Critical</option>
              <option value="shortage">By Shortage Amount</option>
              <option value="category">By Category</option>
              <option value="name">By Name</option>
            </select>
          </div>
        </div>
      </BaseCard>

      <!-- Loading State -->
      <div v-if="loading" class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg overflow-hidden">
        <div class="p-6 space-y-3">
          <div v-for="n in 6" :key="n" class="h-16 bg-neutral-700/50 dark:bg-neutral-700/50 rounded animate-pulse"></div>
        </div>
      </div>

      <!-- Error State -->
      <BaseCard v-else-if="error">
        <div class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-red-500 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-2 text-red-600 dark:text-red-400">{{ error }}</p>
          <BaseButton variant="primary" @click="loadLowStock" class="mt-4">
            Try Again
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Empty State -->
      <BaseCard v-else-if="filteredItems.length === 0">
        <div class="text-center py-12">
          <div class="inline-flex p-4 bg-green-400 dark:bg-green-400 rounded-full mb-4">
            <svg class="h-16 w-16 text-black dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          </div>
          <h3 class="mt-4 text-xl font-semibold text-gray-900 dark:text-white">All Good!</h3>
          <p class="mt-2 text-gray-600 dark:text-gray-300">
            No items are currently low on stock. Great job managing your inventory!
          </p>
        </div>
      </BaseCard>

      <!-- Low Stock Items Table -->
      <div v-else class="hidden md:block">
        <div class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
          <div class="overflow-x-auto custom-scrollbar">
            <table class="min-w-full">
              <thead class="bg-neutral-800/50 dark:bg-neutral-800/50">
                <tr>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    NAME
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    CATEGORY
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    CURRENT STOCK
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    MINIMUM
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    SHORTAGE
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    STATUS
                  </th>
                  <th class="px-6 py-4 text-right text-xs font-bold text-white uppercase tracking-wider">
                    ACTIONS
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in sortedAndFilteredItems"
                  :key="item.id"
                  class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-all duration-200"
                >
                  <td class="px-6 py-5 whitespace-nowrap">
                    <div class="text-sm font-semibold text-white dark:text-white">{{ item.name }}</div>
                    <div v-if="isCritical(item)" class="mt-1">
                      <span class="inline-flex items-center px-2 py-1 text-xs font-bold bg-red-400 dark:bg-red-400 text-black dark:text-black rounded-full animate-pulse">
                        CRITICAL
                      </span>
                    </div>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="px-3 py-1.5 text-xs font-medium bg-neutral-700 dark:bg-neutral-700 text-gray-300 dark:text-gray-300 rounded-full">
                      {{ item.category_name }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <StockBadge
                      :current="item.current_stock"
                      :minimum="item.min_stock_level"
                      :show-percentage="false"
                    />
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ item.min_stock_level }} {{ item.unit }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm font-semibold text-red-400 dark:text-red-400">
                      {{ item.shortage_amount || (item.min_stock_level - item.current_stock) }} {{ item.unit }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span
                      v-if="isCritical(item)"
                      class="inline-flex items-center px-3 py-1.5 text-xs font-bold bg-red-400 dark:bg-red-400 text-black dark:text-black rounded-full"
                    >
                      <span class="w-2 h-2 bg-black dark:bg-black rounded-full mr-2"></span>
                      Out of Stock
                    </span>
                    <span
                      v-else
                      class="inline-flex items-center px-3 py-1.5 text-xs font-bold bg-yellow-400 dark:bg-yellow-400 text-black dark:text-black rounded-full"
                    >
                      <span class="w-2 h-2 bg-black dark:bg-black rounded-full mr-2"></span>
                      Low Stock
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap text-right">
                    <div class="flex items-center justify-end gap-2">
                      <button
                        @click="openRequisitionModal(item)"
                        class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 rounded-lg p-2 transition-colors duration-200"
                        title="Create Requisition"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </button>
                      <button
                        @click="openReceiptModal(item)"
                        class="text-green-500 dark:text-green-400 hover:text-green-400 dark:hover:text-green-300 rounded-lg p-2 transition-colors duration-200"
                        title="Quick Receipt"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Mobile Card View -->
      <div v-if="!loading && !error && filteredItems.length > 0" class="md:hidden space-y-4">
        <div
          v-for="item in sortedAndFilteredItems"
          :key="item.id"
          class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl p-4 border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex-1">
              <h4 class="font-semibold text-white dark:text-white">{{ item.name }}</h4>
              <div v-if="isCritical(item)" class="mt-1">
                <span class="inline-flex items-center px-2 py-1 text-xs font-bold bg-red-400 dark:bg-red-400 text-black dark:text-black rounded-full">
                  CRITICAL
                </span>
              </div>
            </div>
              <StockBadge
                :current="item.current_stock"
                :minimum="item.min_stock_level"
              :show-percentage="false"
              />
          </div>
          <div class="space-y-2 text-sm">
            <div class="flex items-center justify-between">
              <span class="text-gray-300 dark:text-gray-300">Category:</span>
              <span class="px-2 py-1 text-xs font-medium bg-neutral-700 dark:bg-neutral-700 text-gray-300 dark:text-gray-300 rounded-full">
                {{ item.category_name }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-300 dark:text-gray-300">Minimum:</span>
              <span class="text-white dark:text-white">{{ item.min_stock_level }} {{ item.unit }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-300 dark:text-gray-300">Shortage:</span>
              <span class="font-semibold text-red-400 dark:text-red-400">
                {{ item.shortage_amount || (item.min_stock_level - item.current_stock) }} {{ item.unit }}
              </span>
            </div>
          </div>
          <div class="flex gap-2 mt-4 pt-4 border-t border-neutral-700 dark:border-neutral-700">
            <BaseButton
              variant="primary"
              @click="openRequisitionModal(item)"
              class="flex-1 text-sm py-2"
            >
              Requisition
            </BaseButton>
            <BaseButton
              variant="secondary"
              @click="openReceiptModal(item)"
              class="flex-1 text-sm py-2"
            >
              Receipt
            </BaseButton>
          </div>
        </div>
      </div>

      <!-- Create Requisition Modal -->
      <BaseModal :show="showRequisitionModal" title="Create Requisition" @close="closeRequisitionModal">
        <RequisitionForm
          v-if="selectedItem"
          :item="selectedItem"
          :loading="requisitionLoading"
          @submit="handleCreateRequisition"
          @cancel="closeRequisitionModal"
        />
      </BaseModal>

      <!-- Quick Receipt Modal -->
      <BaseModal :show="showReceiptModal" title="Quick Receipt" @close="closeReceiptModal">
        <QuickStockForm
          v-if="selectedItem"
          :item-id="selectedItem.id"
          :item-name="selectedItem.name"
          :current-stock="selectedItem.current_stock"
          :unit="selectedItem.unit"
          movement-type="receipt"
          :loading="receiptLoading"
          @submit="handleQuickReceipt"
          @cancel="closeReceiptModal"
        />
      </BaseModal>

      <!-- Batch Requisition Modal -->
      <BaseModal :show="showBatchRequisitionModal" title="Create Requisitions for All Items" @close="closeBatchModal">
        <div class="space-y-4">
          <p class="text-gray-700">
            This will create requisitions for all {{ filteredItems.length }} low stock items with suggested quantities.
          </p>
          <div class="p-4 bg-blue-50 border border-blue-200 rounded-md">
            <p class="text-sm text-blue-800">
              <strong>Note:</strong> Each requisition will use the shortage amount (minimum - current) as the suggested quantity.
            </p>
          </div>
          <div class="flex justify-end gap-3 pt-4 border-t">
            <BaseButton variant="secondary" @click="closeBatchModal" :disabled="batchActionLoading">
              Cancel
            </BaseButton>
            <BaseButton
              variant="primary"
              @click="handleBatchRequisitions"
              :loading="batchActionLoading"
              :disabled="batchActionLoading"
            >
              Create All Requisitions
            </BaseButton>
          </div>
        </div>
      </BaseModal>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import StockBadge from '../components/StockBadge.vue'
import RequisitionForm from '../components/RequisitionForm.vue'
import QuickStockForm from '../components/QuickStockForm.vue'

const store = useInventoryStore()
const toast = useToast()

// State
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedCategory = ref('')
const sortBy = ref('critical')
const refreshInterval = ref(null)
const requisitionLoading = ref(false)
const receiptLoading = ref(false)
const batchActionLoading = ref(false)

// Modal states
const showRequisitionModal = ref(false)
const showReceiptModal = ref(false)
const showBatchRequisitionModal = ref(false)
const selectedItem = ref(null)

// Computed
const lowStockItems = computed(() => store.lowStockItems)
const items = computed(() => store.items)
const requisitions = computed(() => store.requisitions)

const summaryText = computed(() => {
  const count = filteredItems.value.length
  if (count === 0) return 'No items need reordering at the moment.'
  if (count === 1) return '1 item needs reordering.'
  return `${count} items need reordering.`
})

const criticalItems = computed(() => {
  return lowStockItems.value.filter(item => item.current_stock === 0)
})

const categories = computed(() => {
  const cats = new Set(lowStockItems.value.map(item => item.category_name))
  return Array.from(cats).sort()
})

const filteredItems = computed(() => {
  let result = [...lowStockItems.value]

  // Search filter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    result = result.filter(item => item.name.toLowerCase().includes(query))
  }

  // Category filter (by name)
  if (selectedCategory.value) {
    result = result.filter(item => item.category_name === selectedCategory.value)
  }

  // Hide items with pending requisitions (automatically enabled)
  result = result.filter(item => {
    return !requisitions.value.some(req =>
      (req.item_id === item.id || req.item?.id === item.id) && 
      (req.status === 'pending' || req.status === 'awaiting_delivery')
    )
  })

  return result
})

const sortedAndFilteredItems = computed(() => {
  const result = [...filteredItems.value]

  switch (sortBy.value) {
    case 'critical':
      // Most critical first (lowest stock percentage)
      result.sort((a, b) => {
        const aPercent = (a.current_stock / a.min_stock_level) * 100
        const bPercent = (b.current_stock / b.min_stock_level) * 100
        return aPercent - bPercent
      })
      break
    case 'shortage':
      // By shortage amount (largest shortage first)
      result.sort((a, b) => {
        const aShortage = a.shortage_amount || (a.min_stock_level - a.current_stock)
        const bShortage = b.shortage_amount || (b.min_stock_level - b.current_stock)
        return bShortage - aShortage
      })
      break
    case 'category':
      // By category, then by name
      result.sort((a, b) => {
        if (a.category !== b.category) {
          return a.category.localeCompare(b.category)
        }
        return a.name.localeCompare(b.name)
      })
      break
    case 'name':
      // By name
      result.sort((a, b) => a.name.localeCompare(b.name))
      break
  }

  return result
})

// Methods
const loadLowStock = async () => {
  loading.value = true
  error.value = null
  try {
    await store.fetchLowStock()
    // Also fetch requisitions to check for pending ones
    await store.fetchRequisitions()
  } catch (err) {
    error.value = err.message || 'Failed to load low stock items'
    toast.error('Failed to load low stock items')
  } finally {
    loading.value = false
  }
}

const getItemPriorityClass = (item) => {
  if (item.current_stock === 0) {
    return 'border-l-4 border-red-500'
  }
  const percent = (item.current_stock / item.min_stock_level) * 100
  if (percent < 50) {
    return 'border-l-4 border-orange-500'
  }
  return 'border-l-4 border-yellow-500'
}

const getProgressBarColor = (item) => {
  if (item.current_stock === 0) {
    return 'bg-red-500'
  }
  const percent = (item.current_stock / item.min_stock_level) * 100
  if (percent < 50) {
    return 'bg-orange-500'
  }
  return 'bg-yellow-500'
}

const isCritical = (item) => {
  return item.current_stock === 0
}

const getLastMovementDate = (item) => {
  const movements = store.stockMovements.filter(m => 
    m.item_id === item.id || m.item?.id === item.id
  )
  if (movements.length === 0) return null
  
  const sorted = movements.sort((a, b) => new Date(b.date) - new Date(a.date))
  return sorted[0].date
}

const formatRelativeDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffDays = Math.floor(diffMs / 86400000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffMins = Math.floor(diffMs / 60000)

  if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const openRequisitionModal = (item) => {
  selectedItem.value = item
  showRequisitionModal.value = true
}

const closeRequisitionModal = () => {
  showRequisitionModal.value = false
  selectedItem.value = null
}

const openReceiptModal = (item) => {
  selectedItem.value = item
  showReceiptModal.value = true
}

const closeReceiptModal = () => {
  showReceiptModal.value = false
  selectedItem.value = null
}

const closeBatchModal = () => {
  showBatchRequisitionModal.value = false
}

const handleCreateRequisition = async (formData) => {
  requisitionLoading.value = true
  try {
    await store.createRequisition(formData)
    toast.success('Requisition created successfully')
    closeRequisitionModal()
    await loadLowStock()
    await store.fetchRequisitions()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to create requisition'
    toast.error(errorMessage)
  } finally {
    requisitionLoading.value = false
  }
}

const handleQuickReceipt = async (formData) => {
  receiptLoading.value = true
  try {
    await store.addStockMovement(formData)
    toast.success('Stock receipt added successfully')
    closeReceiptModal()
    await loadLowStock()
    await store.fetchItems()
    await store.fetchStockMovements()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to add receipt'
    toast.error(errorMessage)
  } finally {
    receiptLoading.value = false
  }
}

const handleBatchRequisitions = async () => {
  if (filteredItems.value.length === 0) return

  batchActionLoading.value = true
  try {
    const promises = filteredItems.value.map(item => {
      const quantity = item.shortage_amount || (item.min_stock_level - item.current_stock)
      return store.createRequisition({
        item_id: item.id,
        quantity_requested: quantity,
        requested_by: 'System (Batch)',
        status: 'pending'
      })
    })

    await Promise.all(promises)
    toast.success(`Created ${filteredItems.value.length} requisition(s) successfully`)
    closeBatchModal()
    await loadLowStock()
    await store.fetchRequisitions()
  } catch (err) {
    toast.error('Failed to create some requisitions')
    console.error('Batch requisition error:', err)
  } finally {
    batchActionLoading.value = false
  }
}

const exportToCSV = () => {
  if (filteredItems.value.length === 0) {
    toast.warning('No items to export')
    return
  }

  const headers = [
    'Item Name',
    'Category',
    'Current Stock',
    'Minimum Stock',
    'Shortage',
    'Unit',
    'Stock Percentage',
    'Priority'
  ]

  const rows = sortedAndFilteredItems.value.map(item => {
    const percent = Math.round((item.current_stock / item.min_stock_level) * 100)
    const shortage = item.shortage_amount || (item.min_stock_level - item.current_stock)
    let priority = 'Low'
    if (item.current_stock === 0) priority = 'Critical'
    else if (percent < 50) priority = 'High'
    else priority = 'Medium'

    return [
      item.name,
      item.category_name,
      item.current_stock,
      item.min_stock_level,
      shortage,
      item.unit,
      `${percent}%`,
      priority
    ]
  })

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `low-stock-report-${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  toast.success('Report exported successfully')
}

// Lifecycle
onMounted(async () => {
  await loadLowStock()
  // Load stock movements to get last movement dates
  try {
    await store.fetchStockMovements({ ordering: '-date' })
  } catch (err) {
    console.error('Failed to load stock movements:', err)
  }

  // Set up auto-refresh every 60 seconds
  refreshInterval.value = setInterval(() => {
    loadLowStock()
  }, 60000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
/* Remove all table borders */
table {
  border-collapse: collapse;
}

tbody tr {
  border: none !important;
}

tbody td {
  border: none !important;
}
@page {
  margin: 1cm;
}

@media print {
  .no-print {
    display: none;
  }
}
</style>

