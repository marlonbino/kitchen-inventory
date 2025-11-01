<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <!-- Page Header -->
      <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Items</h1>
          <p class="text-gray-600 mt-1">Manage your inventory items</p>
        </div>
        <BaseButton
          variant="primary"
          @click="openAddModal"
        >
          <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Add New Item
        </BaseButton>
      </div>

      <!-- Filters Section -->
      <BaseCard class="mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Search -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by name..."
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <svg
                class="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
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
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              v-model="selectedCategory"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
            >
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <!-- Unit Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unit</label>
            <select
              v-model="selectedUnit"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
            >
              <option value="">All Units</option>
              <option v-for="unit in units" :key="unit.value" :value="unit.value">
                {{ unit.label }}
              </option>
            </select>
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
        <div class="text-center py-12 px-6">
          <svg class="mx-auto h-16 w-16 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 class="mt-4 text-2xl font-bold text-gray-800">Oops! Something went wrong.</h2>
          <p class="mt-2 text-gray-600">We encountered an error while trying to load your inventory items.</p>

          <div class="mt-6 text-left bg-red-50 p-4 rounded-lg">
            <p class="font-semibold text-red-800">Error Details:</p>
            <p class="text-sm text-red-700 break-words">{{ error }}</p>
          </div>

          <div class="mt-6 text-left space-y-4">
            <div>
              <p class="font-semibold text-gray-700">Possible Causes:</p>
              <ul class="list-disc list-inside text-sm text-gray-600">
                <li>The server might be temporarily unavailable.</li>
                <li>Your device may have lost its network connection.</li>
                <li>The requested data might be malformed or incomplete.</li>
              </ul>
            </div>
            <div>
              <p class="font-semibold text-gray-700">What you can do:</p>
              <ul class="list-disc list-inside text-sm text-gray-600">
                <li>Wait a few moments and then click "Try Again".</li>
                <li>Check your internet connection.</li>
                <li>If the problem persists, please contact our support team.</li>
              </ul>
            </div>
          </div>

          <BaseButton variant="primary" @click="loadItems" class="mt-8">
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h5" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 20v-5h-5" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 20L9 15M20 4l-5 5" />
            </svg>
            Try Again
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Empty State -->
      <BaseCard v-else-if="filteredItems.length === 0">
        <EmptyState
          title="No Items Found"
          message="Get started by adding a new item to your inventory."
          button-text="Add New Item"
          @button-click="openAddModal"
        />
      </BaseCard>

      <!-- Desktop Table View -->
      <div v-else class="hidden md:block">
        <BaseCard>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    @click="sortBy('name')"
                  >
                    <div class="flex items-center gap-2">
                      Name
                      <svg v-if="sortField === 'name'" class="w-4 h-4" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                    </div>
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    @click="sortBy('category')"
                  >
                    <div class="flex items-center gap-2">
                      Category
                      <svg v-if="sortField === 'category'" class="w-4 h-4" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                    </div>
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Unit
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    @click="sortBy('current_stock')"
                  >
                    <div class="flex items-center gap-2">
                      Current Stock
                      <svg v-if="sortField === 'current_stock'" class="w-4 h-4" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                    </div>
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Minimum
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="item in filteredItems"
                  :key="item.id"
                  class="hover:bg-gray-50 transition-colors"
                >
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">{{ item.name || 'N/A' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded">
                      {{ item.category || 'N/A' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ item.unit || 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <StockBadge
                      :current="item.current_stock != null ? item.current_stock : 0"
                      :minimum="item.min_stock_level != null ? item.min_stock_level : 0"
                      :show-percentage="false"
                    />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ item.min_stock_level != null ? item.min_stock_level : 'N/A' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      v-if="item.is_low_stock"
                      class="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full"
                    >
                      Low Stock
                    </span>
                    <span
                      v-else
                      class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full"
                    >
                      OK
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex items-center justify-end gap-2">
                      <button
                        @click="openEditModal(item)"
                        class="text-blue-600 hover:text-blue-900"
                        title="Edit"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        @click="openQuickReceipt(item)"
                        class="text-green-600 hover:text-green-900"
                        title="Quick Receipt"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                      </button>
                      <button
                        @click="openQuickIssue(item)"
                        class="text-red-600 hover:text-red-900"
                        title="Quick Issue"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                        </svg>
                      </button>
                      <button
                        @click="openDeleteConfirm(item)"
                        class="text-red-600 hover:text-red-900"
                        title="Delete"
                        aria-label="Delete item"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </BaseCard>
      </div>

      <!-- Mobile Card View -->
      <div v-if="!loading && !error && filteredItems.length > 0" class="md:hidden space-y-4">
        <BaseCard
          v-for="item in filteredItems"
          :key="item.id"
          class="hover:shadow-lg transition-shadow"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900">{{ item.name }}</h3>
              <div class="flex items-center gap-2 mt-1">
                <span class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded">
                  {{ item.category }}
                </span>
                <span class="text-sm text-gray-500">{{ item.unit }}</span>
              </div>
            </div>
            <StockBadge
              :current="item.current_stock"
              :minimum="item.min_stock_level"
              :show-percentage="false"
            />
          </div>

          <div class="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div>
              <span class="text-gray-500">Minimum:</span>
              <span class="ml-2 font-medium">{{ item.min_stock_level }}</span>
            </div>
            <div>
              <span class="text-gray-500">Status:</span>
              <span
                :class="item.is_low_stock ? 'text-red-600' : 'text-green-600'"
                class="ml-2 font-medium"
              >
                {{ item.is_low_stock ? 'Low Stock' : 'OK' }}
              </span>
            </div>
          </div>

          <div class="flex gap-2 pt-3 border-t">
            <BaseButton
              variant="secondary"
              @click="openEditModal(item)"
              class="flex-1 text-sm py-2"
            >
              Edit
            </BaseButton>
            <BaseButton
              variant="primary"
              @click="openQuickReceipt(item)"
              class="flex-1 text-sm py-2"
            >
              Receipt
            </BaseButton>
            <BaseButton
              variant="danger"
              @click="openDeleteConfirm(item)"
              class="flex-1 text-sm py-2"
            >
              Delete
            </BaseButton>
          </div>
        </BaseCard>
      </div>

      <!-- Add/Edit Item Modal -->
      <BaseModal
        :show="showItemModal"
        :title="editingItem ? 'Edit Item' : 'Add New Item'"
        @close="closeItemModal"
      >
        <ItemForm
          :item="editingItem"
          :loading="itemLoading"
          :submit-text="editingItem ? 'Update Item' : 'Create Item'"
          @submit="handleItemSubmit"
          @cancel="closeItemModal"
        />
      </BaseModal>

      <!-- Quick Receipt Modal -->
      <BaseModal
        :show="showReceiptModal"
        title="Quick Receipt"
        @close="closeReceiptModal"
      >
        <QuickStockForm
          v-if="selectedItem"
          :item-id="selectedItem.id"
          :item-name="selectedItem.name"
          :current-stock="selectedItem.current_stock"
          :unit="selectedItem.unit"
          movement-type="receipt"
          :loading="movementLoading"
          @submit="handleQuickReceipt"
          @cancel="closeReceiptModal"
        />
      </BaseModal>

      <!-- Quick Issue Modal -->
      <BaseModal
        :show="showIssueModal"
        title="Quick Issue"
        @close="closeIssueModal"
      >
        <QuickStockForm
          v-if="selectedItem"
          :item-id="selectedItem.id"
          :item-name="selectedItem.name"
          :current-stock="selectedItem.current_stock"
          :unit="selectedItem.unit"
          movement-type="issue"
          :loading="movementLoading"
          @submit="handleQuickIssue"
          @cancel="closeIssueModal"
        />
      </BaseModal>

      <!-- Delete Confirmation Dialog -->
      <ConfirmDialog
        :show="showDeleteConfirm"
        title="Delete Item"
        :message="getDeleteMessage()"
        confirm-text="Delete"
        cancel-text="Cancel"
        variant="danger"
        @confirm="handleDeleteConfirm"
        @cancel="cancelDelete"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import { useDebounce } from '../composables/useDebounce'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import StockBadge from '../components/StockBadge.vue'
import ItemForm from '../components/ItemForm.vue'
import QuickStockForm from '../components/QuickStockForm.vue'

const store = useInventoryStore()
const toast = useToast()

// State
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const debouncedSearchQuery = useDebounce(searchQuery, 300)
const selectedCategory = ref('')
const selectedUnit = ref('')
const sortField = ref('name')
const sortDirection = ref('asc')

// Modal states
const showItemModal = ref(false)
const showReceiptModal = ref(false)
const showIssueModal = ref(false)
const showDeleteConfirm = ref(false)
const editingItem = ref(null)
const selectedItem = ref(null)
const itemToDelete = ref(null)
const itemLoading = ref(false)
const movementLoading = ref(false)

// Constants
const categories = ['Produce', 'Dairy', 'Pantry', 'Meat', 'Spices', 'Frozen', 'Other']
const units = [
  { value: 'kg', label: 'Kilogram' },
  { value: 'g', label: 'Gram' },
  { value: 'lb', label: 'Pound' },
  { value: 'oz', label: 'Ounce' },
  { value: 'piece', label: 'Piece' },
  { value: 'bottle', label: 'Bottle' },
  { value: 'pack', label: 'Pack' }
]

// Computed
const items = computed(() => store.items)
const loadingState = computed(() => store.loading.items)

const filteredItems = computed(() => {
  let result = [...items.value]

  // Search filter (using debounced value)
  if (debouncedSearchQuery.value.trim()) {
    const query = debouncedSearchQuery.value.toLowerCase().trim()
    result = result.filter(item =>
      item.name.toLowerCase().includes(query)
    )
  }

  // Category filter
  if (selectedCategory.value) {
    result = result.filter(item => item.category === selectedCategory.value)
  }

  // Unit filter
  if (selectedUnit.value) {
    result = result.filter(item => item.unit === selectedUnit.value)
  }

  // Sorting
  result.sort((a, b) => {
    let aVal = a[sortField.value]
    let bVal = b[sortField.value]

    // Handle string comparison
    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase()
      bVal = bVal.toLowerCase()
    }

    if (sortDirection.value === 'asc') {
      return aVal > bVal ? 1 : aVal < bVal ? -1 : 0
    } else {
      return aVal < bVal ? 1 : aVal > bVal ? -1 : 0
    }
  })

  return result
})

// Methods
const loadItems = async () => {
  loading.value = true
  error.value = null
  try {
    await store.fetchItems()
  } catch (err) {
    error.value = err.message || 'Failed to load items'
    toast.error('Failed to load items')
  } finally {
    loading.value = false
  }
}

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }
}

// Modal handlers
const openAddModal = () => {
  editingItem.value = null
  showItemModal.value = true
}

const openEditModal = (item) => {
  editingItem.value = item
  showItemModal.value = true
}

const closeItemModal = () => {
  showItemModal.value = false
  editingItem.value = null
}

const openQuickReceipt = (item) => {
  selectedItem.value = item
  showReceiptModal.value = true
}

const closeReceiptModal = () => {
  showReceiptModal.value = false
  selectedItem.value = null
}

const openQuickIssue = (item) => {
  selectedItem.value = item
  showIssueModal.value = true
}

const closeIssueModal = () => {
  showIssueModal.value = false
  selectedItem.value = null
}

const openDeleteConfirm = (item) => {
  itemToDelete.value = item
  showDeleteConfirm.value = true
}

const cancelDelete = () => {
  showDeleteConfirm.value = false
  itemToDelete.value = null
}

const getDeleteMessage = () => {
  if (!itemToDelete.value) return ''
  return `Are you sure you want to delete "${itemToDelete.value.name}"?\n\nThis action cannot be undone and will affect inventory tracking.`
}

// Form handlers
const handleItemSubmit = async (formData) => {
  itemLoading.value = true
  try {
    if (editingItem.value) {
      await store.updateItem(editingItem.value.id, formData)
      toast.success('Item updated successfully')
    } else {
      await store.addItem(formData)
      toast.success('Item created successfully')
    }
    closeItemModal()
    // Reload items to get updated data
    await loadItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to save item'
    toast.error(errorMessage)
  } finally {
    itemLoading.value = false
  }
}

const handleQuickReceipt = async (formData) => {
  movementLoading.value = true
  try {
    await store.addStockMovement(formData)
    toast.success('Stock receipt added successfully')
    closeReceiptModal()
    // Reload items to update stock levels
    await loadItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to add receipt'
    toast.error(errorMessage)
  } finally {
    movementLoading.value = false
  }
}

const handleQuickIssue = async (formData) => {
  movementLoading.value = true
  try {
    await store.addStockMovement(formData)
    toast.success('Stock issued successfully')
    closeIssueModal()
    // Reload items to update stock levels
    await loadItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to issue stock'
    toast.error(errorMessage)
  } finally {
    movementLoading.value = false
  }
}

const handleDeleteConfirm = async () => {
  if (!itemToDelete.value) return
  
  itemLoading.value = true
  try {
    await store.removeItem(itemToDelete.value.id)
    toast.success(`Item "${itemToDelete.value.name}" deleted successfully!`)
    await loadItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to delete item'
    toast.error(errorMessage)
  } finally {
    itemLoading.value = false
    cancelDelete()
  }
}

// Lifecycle
onMounted(() => {
  loadItems()
})
</script>

