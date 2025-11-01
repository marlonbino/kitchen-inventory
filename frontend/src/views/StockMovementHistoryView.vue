<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-4 md:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <!-- Page Header -->
      <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Stock Movements</h1>
          <p class="text-gray-600 dark:text-gray-300 mt-1">History of all stock movements</p>
        </div>
        <div class="flex gap-2">
          <BaseButton
            variant="secondary"
            @click="exportToCSV"
            :disabled="loading || movements.length === 0"
          >
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export CSV
          </BaseButton>
          <BaseButton variant="primary" @click="openRecordModal">
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Record Movement
          </BaseButton>
        </div>
      </div>

      <!-- Filters Section -->
      <BaseCard class="mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Movement Type Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Movement Type</label>
            <select
              v-model="filters.movement_type"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
            >
              <option value="">All Types</option>
              <option value="receipt">Receipt</option>
              <option value="issue">Issue</option>
              <option value="writeoff">Write-off</option>
            </select>
          </div>

          <!-- Item Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Item</label>
            <select
              v-model="filters.item"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
            >
              <option value="">All Items</option>
              <option v-for="item in items" :key="item.id" :value="item.id">
                {{ item.name }}
              </option>
            </select>
          </div>

          <!-- Date From -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date From</label>
            <input
              v-model="filters.date_from"
              type="date"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
            />
          </div>

          <!-- Date To -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date To</label>
            <input
              v-model="filters.date_to"
              type="date"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
            />
          </div>
        </div>
      </BaseCard>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div v-for="n in 5" :key="n" class="bg-white rounded-lg shadow-md p-6 animate-pulse">
          <div class="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>

      <!-- Error State -->
      <BaseCard v-else-if="error">
        <div class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-2 text-red-600">{{ error }}</p>
          <BaseButton variant="primary" @click="loadMovements" class="mt-4">
            Try Again
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Empty State -->
      <BaseCard v-else-if="filteredMovements.length === 0">
        <div class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="mt-2 text-gray-500">No stock movements found</p>
          <BaseButton variant="primary" @click="openRecordModal" class="mt-4">
            Record First Movement
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Movements Table -->
      <div v-else class="hidden md:block">
        <div class="bg-neutral-800 dark:bg-neutral-800 rounded-xl shadow-elegant overflow-hidden border border-neutral-700 dark:border-neutral-700">
          <div class="overflow-x-auto custom-scrollbar">
            <table class="min-w-full divide-y divide-neutral-700 dark:divide-neutral-700">
              <thead class="bg-neutral-800 dark:bg-neutral-800 border-b-2 border-neutral-700 dark:border-neutral-700">
                <tr>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    DATE
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    ITEM
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    TYPE
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    QTY
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    REF
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    STOCK AFTER
                  </th>
                  <th class="px-6 py-4 text-right text-xs font-bold text-white uppercase tracking-wider">
                    ACTIONS
                  </th>
                </tr>
              </thead>
              <tbody class="bg-neutral-800 dark:bg-neutral-800 divide-y divide-neutral-700 dark:divide-neutral-700">
                <tr
                  v-for="movement in paginatedMovements"
                  :key="movement.id"
                  class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-colors duration-150"
                >
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ formatDateTime(movement.date) }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <div class="text-sm font-semibold text-white dark:text-white">
                      {{ movement.item_name || movement.item?.name || 'Unknown' }}
                    </div>
                    <div class="text-xs text-gray-400 dark:text-gray-400 mt-0.5">
                      {{ getItemCategory(movement) }}
                    </div>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-3 py-1.5 text-xs font-bold rounded-full"
                      :class="getMovementTypeBadgeClassDark(movement.movement_type)"
                    >
                      {{ getMovementTypeLabel(movement.movement_type) }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span
                      class="text-sm font-medium"
                      :class="getQuantityClassDark(movement.movement_type)"
                    >
                      {{ getQuantityPrefix(movement.movement_type) }}{{ movement.quantity }}
                      {{ getItemUnit(movement) }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ movement.reference || '—' }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm font-medium text-gray-300 dark:text-gray-300">
                      {{ getRunningBalance(movement) }} {{ getItemUnit(movement) }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap text-right">
                    <div class="flex items-center justify-end gap-2">
                      <button
                        @click="viewDetails(movement)"
                        class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 rounded-lg p-2 transition-colors duration-200"
                        title="View Details"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </button>
                      <button
                        @click="confirmDelete(movement)"
                        class="text-red-500 dark:text-red-400 hover:text-red-400 dark:hover:text-red-300 rounded-lg p-2 transition-colors duration-200"
                        title="Delete"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div
            v-if="totalPages > 1"
            class="px-6 py-4 border-t border-neutral-700 dark:border-neutral-700 flex items-center justify-between bg-neutral-800 dark:bg-neutral-800"
          >
          <div class="text-sm text-gray-300 dark:text-gray-300">
            Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ filteredMovements.length }} movements
          </div>
          <div class="flex gap-2">
            <BaseButton
              variant="secondary"
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
            >
              Previous
            </BaseButton>
            <span class="px-4 py-2 text-sm text-gray-300 dark:text-gray-300">
              Page {{ currentPage }} of {{ totalPages }}
            </span>
            <BaseButton
              variant="secondary"
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
            >
              Next
            </BaseButton>
          </div>
        </div>
      </BaseCard>

      <!-- Record Movement Modal -->
      <BaseModal :show="showRecordModal" title="Record Stock Movement" @close="closeRecordModal">
        <StockMovementForm
          :loading="movementLoading"
          @submit="handleRecordMovement"
          @cancel="closeRecordModal"
        />
      </BaseModal>

      <!-- View Details Modal -->
      <BaseModal :show="showDetailsModal" title="Movement Details" @close="closeDetailsModal">
        <div v-if="selectedMovement" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium text-gray-500">Date/Time</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDateTime(selectedMovement.date) }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Movement Type</label>
              <p class="mt-1">
                <span
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="getMovementTypeBadgeClass(selectedMovement.movement_type)"
                >
                  {{ getMovementTypeLabel(selectedMovement.movement_type) }}
                </span>
              </p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Item</label>
              <p class="mt-1 text-sm text-gray-900">
                {{ selectedMovement.item_name || selectedMovement.item?.name || 'Unknown' }}
              </p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Quantity</label>
              <p
                class="mt-1 text-sm font-medium"
                :class="getQuantityClass(selectedMovement.movement_type)"
              >
                {{ getQuantityPrefix(selectedMovement.movement_type) }}{{ selectedMovement.quantity }}
                {{ getItemUnit(selectedMovement) }}
              </p>
            </div>
            <div v-if="selectedMovement.reference">
              <label class="text-sm font-medium text-gray-500">Reference</label>
              <p class="mt-1 text-sm text-gray-900">{{ selectedMovement.reference }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Stock After Movement</label>
              <p class="mt-1 text-sm font-medium text-gray-900">
                {{ getRunningBalance(selectedMovement) }} {{ getItemUnit(selectedMovement) }}
              </p>
            </div>
          </div>
          <div v-if="selectedMovement.notes">
            <label class="text-sm font-medium text-gray-500">Notes</label>
            <p class="mt-1 text-sm text-gray-900 whitespace-pre-wrap">{{ selectedMovement.notes }}</p>
          </div>
        </div>
      </BaseModal>

      <!-- Delete Confirmation Dialog -->
      <ConfirmDialog
        :show="showDeleteConfirm"
        title="Delete Movement"
        message="Are you sure you want to delete this movement? This action cannot be undone and will affect stock levels."
        confirm-text="Delete"
        cancel-text="Cancel"
        variant="danger"
        @confirm="handleDelete"
        @cancel="cancelDelete"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import { useDebounce } from '../composables/useDebounce'
import { deleteStockMovement } from '../services/api'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import StockMovementForm from '../components/StockMovementForm.vue'

const store = useInventoryStore()
const toast = useToast()

// State
const loading = ref(false)
const error = ref(null)
const movementLoading = ref(false)
const movements = ref([])
const runningBalances = ref({}) // Track running balance per item

// Filters
const filters = reactive({
  movement_type: '',
  item: '',
  date_from: '',
  date_to: ''
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = 20

// Modal states
const showRecordModal = ref(false)
const showDetailsModal = ref(false)
const showDeleteConfirm = ref(false)
const selectedMovement = ref(null)
const movementToDelete = ref(null)

// Computed
const items = computed(() => store.items)
const storeMovements = computed(() => store.stockMovements)

// Load items if not already loaded
watch(() => store.items.length, (newLength) => {
  if (newLength === 0 && !store.loading.items) {
    store.fetchItems().catch(console.error)
  }
})

const filteredMovements = computed(() => {
  let result = [...movements.value]

  // Filter by movement type
  if (filters.movement_type) {
    result = result.filter(m => m.movement_type === filters.movement_type)
  }

  // Filter by item
  if (filters.item) {
    const itemId = parseInt(filters.item)
    result = result.filter(m => m.item_id === itemId || m.item?.id === itemId)
  }

  // Filter by date range
  if (filters.date_from) {
    const fromDate = new Date(filters.date_from)
    fromDate.setHours(0, 0, 0, 0)
    result = result.filter(m => {
      const movementDate = new Date(m.date)
      movementDate.setHours(0, 0, 0, 0)
      return movementDate >= fromDate
    })
  }

  if (filters.date_to) {
    const toDate = new Date(filters.date_to)
    toDate.setHours(23, 59, 59, 999)
    result = result.filter(m => {
      const movementDate = new Date(m.date)
      return movementDate <= toDate
    })
  }

  // Sort by date descending (newest first)
  result.sort((a, b) => new Date(b.date) - new Date(a.date))

  // Calculate running balances
  calculateRunningBalances(result)

  return result
})

const totalPages = computed(() => {
  return Math.ceil(filteredMovements.value.length / itemsPerPage)
})

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage
})

const endIndex = computed(() => {
  return Math.min(startIndex.value + itemsPerPage, filteredMovements.value.length)
})

const paginatedMovements = computed(() => {
  return filteredMovements.value.slice(startIndex.value, endIndex.value)
})

// Methods
const loadMovements = async () => {
  loading.value = true
  error.value = null
  try {
    await store.fetchStockMovements({ ordering: '-date' })
    movements.value = store.stockMovements
  } catch (err) {
    error.value = err.message || 'Failed to load movements'
    toast.error('Failed to load stock movements')
  } finally {
    loading.value = false
  }
}

const calculateRunningBalances = (movementList) => {
  runningBalances.value = {}
  
  // Group movements by item and sort by date ascending
  const itemMovements = {}
  movementList.forEach(m => {
    const itemId = m.item_id || m.item?.id
    if (!itemId) return
    
    if (!itemMovements[itemId]) {
      itemMovements[itemId] = []
    }
    itemMovements[itemId].push(m)
  })

  // For each item, calculate running balance
  Object.keys(itemMovements).forEach(itemId => {
    const sortedMovements = [...itemMovements[itemId]].sort(
      (a, b) => new Date(a.date) - new Date(b.date)
    )
    
    const item = store.itemById(parseInt(itemId))
    let balance = item ? item.current_stock : 0
    
    // Work backwards from current stock
    const balances = {}
    sortedMovements.reverse().forEach(m => {
      balances[m.id] = balance
      if (m.movement_type === 'receipt') {
        balance -= m.quantity
      } else if (['issue', 'writeoff'].includes(m.movement_type)) {
        balance += m.quantity
      }
    })
    
    // Reverse again to get forward-looking balances
    sortedMovements.reverse()
    let forwardBalance = balance
    sortedMovements.forEach(m => {
      if (m.movement_type === 'receipt') {
        forwardBalance += m.quantity
      } else if (['issue', 'writeoff'].includes(m.movement_type)) {
        forwardBalance -= m.quantity
      }
      balances[m.id] = forwardBalance
    })
    
    Object.assign(runningBalances.value, balances)
  })
}

const getRunningBalance = (movement) => {
  return runningBalances.value[movement.id] ?? 0
}

const formatDateTime = (dateString) => {
  if (!dateString) return 'Unknown'
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
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

const getMovementTypeBadgeClass = (type) => {
  const classes = {
    receipt: 'bg-green-100 text-green-800',
    issue: 'bg-blue-100 text-blue-800',
    writeoff: 'bg-red-100 text-red-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const getMovementTypeBadgeClassDark = (type) => {
  const classes = {
    receipt: 'bg-green-400 dark:bg-green-400 text-black dark:text-black',
    issue: 'bg-blue-400 dark:bg-blue-400 text-black dark:text-black',
    writeoff: 'bg-red-400 dark:bg-red-400 text-black dark:text-black'
  }
  return classes[type] || 'bg-gray-400 dark:bg-gray-400 text-black dark:text-black'
}

const getQuantityPrefix = (type) => {
  if (type === 'receipt') return '+'
  if (['issue', 'writeoff'].includes(type)) return '-'
  return ''
}

const getQuantityClass = (type) => {
  if (type === 'receipt') return 'text-green-600'
  if (['issue', 'writeoff'].includes(type)) return 'text-red-600'
  return 'text-gray-600'
}

const getQuantityClassDark = (type) => {
  if (type === 'receipt') return 'text-green-400 dark:text-green-400'
  if (['issue', 'writeoff'].includes(type)) return 'text-red-400 dark:text-red-400'
  return 'text-gray-300 dark:text-gray-300'
}

const getItemUnit = (movement) => {
  const item = store.itemById(movement.item_id || movement.item?.id)
  return item?.unit || 'units'
}

const getItemCategory = (movement) => {
  const item = store.itemById(movement.item_id || movement.item?.id)
  return item?.category || ''
}

const openRecordModal = () => {
  showRecordModal.value = true
}

const closeRecordModal = () => {
  showRecordModal.value = false
}

const handleRecordMovement = async (formData) => {
  movementLoading.value = true
  try {
    await store.addStockMovement(formData)
    toast.success('Movement recorded successfully')
    closeRecordModal()
    await loadMovements()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to record movement'
    toast.error(errorMessage)
  } finally {
    movementLoading.value = false
  }
}

const viewDetails = (movement) => {
  selectedMovement.value = movement
  showDetailsModal.value = true
}

const closeDetailsModal = () => {
  showDetailsModal.value = false
  selectedMovement.value = null
}

const confirmDelete = (movement) => {
  movementToDelete.value = movement
  showDeleteConfirm.value = true
}

const cancelDelete = () => {
  showDeleteConfirm.value = false
  movementToDelete.value = null
}

const handleDelete = async () => {
  if (!movementToDelete.value) return

  try {
    await deleteStockMovement(movementToDelete.value.id)
    toast.success('Movement deleted successfully')
    cancelDelete()
    await loadMovements()
    // Reload items to update stock levels
    await store.fetchItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to delete movement'
    toast.error(errorMessage)
    cancelDelete()
  }
}

const exportToCSV = () => {
  if (filteredMovements.value.length === 0) {
    toast.warning('No movements to export')
    return
  }

  // CSV headers
  const headers = [
    'Date/Time',
    'Item',
    'Movement Type',
    'Quantity',
    'Reference',
    'Notes',
    'Stock After'
  ]

  // CSV rows
  const rows = filteredMovements.value.map(movement => [
    formatDateTime(movement.date),
    movement.item_name || movement.item?.name || 'Unknown',
    getMovementTypeLabel(movement.movement_type),
    `${getQuantityPrefix(movement.movement_type)}${movement.quantity} ${getItemUnit(movement)}`,
    movement.reference || '',
    movement.notes || '',
    `${getRunningBalance(movement)} ${getItemUnit(movement)}`
  ])

  // Combine headers and rows
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
  ].join('\n')

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `stock-movements-${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  toast.success('CSV exported successfully')
}

// Watch filters for debounced updates (simple version - could add debounce)
watch(() => [filters.movement_type, filters.item, filters.date_from, filters.date_to], () => {
  currentPage.value = 1 // Reset to first page when filters change
})

// Lifecycle
onMounted(async () => {
  await loadMovements()
  // Load items if not already loaded
  if (store.items.length === 0) {
    try {
      await store.fetchItems()
    } catch (err) {
      console.error('Failed to load items:', err)
    }
  }
})
</script>

