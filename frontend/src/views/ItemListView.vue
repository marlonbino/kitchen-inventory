<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-3 sm:p-4 md:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Page Header -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-2 bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">Current Stock</h1>
          <p class="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-300 font-medium">View what is available in kitchen now</p>
        </div>
        <BaseButton
          v-if="isAdmin"
          variant="primary"
          @click="openAddModal"
          class="shadow-md"
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
            <label class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Search</label>
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by name..."
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-neutral-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 bg-white dark:bg-neutral-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
              />
              <svg
                class="absolute left-3 top-2.5 h-6 w-6 text-gray-400 dark:text-gray-500"
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
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Unit Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-white mb-1">Unit</label>
            <select
              v-model="selectedUnit"
              class="block w-full px-3 py-2 border border-gray-300 dark:border-neutral-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 bg-white dark:bg-neutral-800 text-gray-900 dark:text-white"
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
        <div class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-2 text-red-600">{{ error }}</p>
          <BaseButton variant="primary" @click="loadItems" class="mt-4">
            Try Again
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Empty State -->
      <BaseCard v-else-if="filteredItems.length === 0">
        <div class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
          <p class="mt-2 text-gray-500">No items found</p>
          <BaseButton variant="primary" @click="openAddModal" class="mt-4">
            Add First Item
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Desktop Table View -->
      <div v-else class="hidden md:block">
        <div class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
          <div class="overflow-x-auto custom-scrollbar">
            <table class="min-w-full">
              <thead class="bg-neutral-800/50 dark:bg-neutral-800/50">
                <tr>
                  <th
                    class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider cursor-pointer hover:bg-neutral-700 dark:hover:bg-neutral-700 transition-colors"
                    @click="sortBy('name')"
                  >
                    <div class="flex items-center gap-2">
                      NAME
                      <svg v-if="sortField === 'name'" class="w-4 h-4 text-blue-500 dark:text-blue-400" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                    </div>
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider cursor-pointer hover:bg-neutral-700 dark:hover:bg-neutral-700 transition-colors"
                    @click="sortBy('category')"
                  >
                    <div class="flex items-center gap-2">
                      CATEGORY
                      <svg v-if="sortField === 'category'" class="w-4 h-4 text-blue-500 dark:text-blue-400" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                    </div>
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    UNIT
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    PRICE (KES)
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider cursor-pointer hover:bg-neutral-700 dark:hover:bg-neutral-700 transition-colors"
                    @click="sortBy('current_stock')"
                  >
                    <div class="flex items-center gap-2">
                      STOCK AVAILABLE
                      <svg v-if="sortField === 'current_stock'" class="w-4 h-4 text-blue-500 dark:text-blue-400" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                    </div>
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    MINIMUM LEVEL
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    VALUE (KES)
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    SUPPLIER
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
                  v-for="item in displayedItems"
                  :key="item.id"
                  class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-all duration-200"
                >
                  <td class="px-6 py-5 whitespace-nowrap">
                    <div class="text-sm font-semibold text-white dark:text-white">{{ item.name }}</div>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="px-3 py-1.5 text-xs font-medium bg-neutral-700 dark:bg-neutral-700 text-gray-300 dark:text-gray-300 rounded-full">
                      {{ item.category_name }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ item.unit }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">
                      {{ item.price_per_unit ? formatCurrency(item.price_per_unit) : '-' }}
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
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ item.min_stock_level }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm font-semibold text-gray-300 dark:text-gray-300">
                      {{ item.total_value ? formatCurrency(item.total_value) : '-' }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ item.supplier || '-' }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span
                      v-if="item.is_low_stock"
                      class="inline-flex items-center px-3 py-1.5 text-xs font-bold bg-red-400 dark:bg-red-400 text-black dark:text-black rounded-full"
                    >
                      <span class="w-2 h-2 bg-black dark:bg-black rounded-full mr-2"></span>
                      Restock Needed
                    </span>
                    <span
                      v-else
                      class="inline-flex items-center px-3 py-1.5 text-xs font-bold bg-green-400 dark:bg-green-400 text-black dark:text-black rounded-full"
                    >
                      <span class="w-2 h-2 bg-black dark:bg-black rounded-full mr-2"></span>
                      OK
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap text-right">
                    <div class="flex items-center justify-end gap-2">
                      <button
                        v-if="isAdmin"
                        @click="openEditModal(item)"
                        class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 rounded-lg p-2 transition-colors duration-200"
                        title="Edit"
                        aria-label="Edit item"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button
                        @click="openQuickReceipt(item)"
                        class="text-green-500 dark:text-green-400 hover:text-green-400 dark:hover:text-green-300 rounded-lg p-2 transition-colors duration-200"
                        title="Receive Delivery"
                        aria-label="Receive delivery"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                      </button>
                      <button
                        @click="openQuickUsage(item)"
                        class="text-orange-500 dark:text-yellow-400 hover:text-orange-400 dark:hover:text-yellow-300 rounded-lg p-2 transition-colors duration-200"
                        title="Track Usage"
                        aria-label="Track usage"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                        </svg>
                      </button>
                      <button
                        v-if="isAdmin"
                        @click="openDeleteConfirm(item)"
                        class="text-red-500 dark:text-red-400 hover:text-red-400 dark:hover:text-red-300 rounded-lg p-2 transition-colors duration-200"
                        title="Delete"
                        aria-label="Delete item"
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
          <!-- Show More / Show Less Button -->
          <div v-if="filteredItems.length > 0" class="px-6 py-4 bg-neutral-800/50 dark:bg-neutral-800/50">
            <div class="flex items-center justify-center gap-3">
              <button
                v-if="hasMoreItems"
                @click="showMore"
                class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
              >
                See More ({{ filteredItems.length - itemsToShow }} remaining)
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <button
                v-if="showLessButton"
                @click="showLess"
                class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
              >
                Show Less
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile Card View -->
      <div v-if="!loading && !error && filteredItems.length > 0" class="md:hidden space-y-4">
        <BaseCard
          v-for="item in displayedItems"
          :key="item.id"
          class="hover:shadow-lg transition-shadow"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ item.name }}</h3>
              <div class="flex items-center gap-2 mt-1">
                <span class="px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-neutral-700 text-gray-800 dark:text-gray-300 rounded">
                  {{ item.category_name }}
                </span>
                <span class="text-sm text-gray-500 dark:text-gray-400">{{ item.unit }}</span>
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
              <span class="text-gray-500 dark:text-gray-400">Minimum:</span>
              <span class="ml-2 font-medium dark:text-gray-300">{{ item.min_stock_level }}</span>
            </div>
            <div>
              <span class="text-gray-500 dark:text-gray-400">Status:</span>
              <span
                :class="item.is_low_stock ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'"
                class="ml-2 font-medium"
              >
                {{ item.is_low_stock ? 'Low Stock' : 'OK' }}
              </span>
            </div>
          </div>

          <div class="flex gap-2 pt-3 border-t dark:border-neutral-700">
            <BaseButton
              v-if="isAdmin"
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
              v-if="isAdmin"
              variant="danger"
              @click="openDeleteConfirm(item)"
              class="flex-1 text-sm py-2"
            >
              Delete
            </BaseButton>
          </div>
        </BaseCard>
        <!-- Show More / Show Less Button (Mobile) -->
        <div v-if="filteredItems.length > 0" class="flex items-center justify-center gap-3 pt-2">
          <button
            v-if="hasMoreItems"
            @click="showMore"
            class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
          >
            See More ({{ filteredItems.length - itemsToShow }} remaining)
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <button
            v-if="showLessButton"
            @click="showLess"
            class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
          >
            Show Less
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Add/Edit Item Modal -->
      <BaseModal
        :show="showItemModal"
        :title="editingItem ? 'Edit Item Details' : 'Add New Item to System'"
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
        title="Record Purchase Delivery"
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
        :show="showUsageModal"
        title="Quick Usage Tracking"
        @close="closeUsageModal"
      >
        <QuickStockForm
          v-if="selectedItem"
          :item-id="selectedItem.id"
          :item-name="selectedItem.name"
          :current-stock="selectedItem.current_stock"
          :unit="selectedItem.unit"
          movement-type="usage"
          :loading="movementLoading"
          @submit="handleQuickUsage"
          @cancel="closeUsageModal"
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
import { getCategories, getUserInfo } from '../services/api.js'

const store = useInventoryStore()
const toast = useToast()

// Current user info
const currentUser = ref(null)
const isAdmin = computed(() => currentUser.value?.role === 'admin')

// State
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const debouncedSearchQuery = useDebounce(searchQuery, 300)
const selectedCategory = ref('')
const selectedUnit = ref('')
const itemsToShow = ref(5)
const sortField = ref('name')
const sortDirection = ref('asc')

// Modal states
const showItemModal = ref(false)
const showReceiptModal = ref(false)
const showUsageModal = ref(false)
const showDeleteConfirm = ref(false)
const editingItem = ref(null)
const selectedItem = ref(null)
const itemToDelete = ref(null)
const itemLoading = ref(false)
const movementLoading = ref(false)

// State for categories
const categories = ref([])

// Load categories on mount
onMounted(async () => {
  try {
    const cats = await getCategories()
    categories.value = cats
  } catch (error) {
    console.error('Error loading categories:', error)
  }
  
  // Load user info
  try {
    const user = await getUserInfo()
    currentUser.value = user
  } catch (error) {
    console.error('Failed to get user info:', error)
  }
})

const units = [
  { value: 'kg', label: 'Kilogram (Kg)' },
  { value: 'litre', label: 'Litre (L)' },
  { value: 'piece', label: 'Piece' },
  { value: 'packet', label: 'Packet' },
  { value: 'dozen', label: 'Dozen' },
  { value: 'bale', label: 'Bale' }
]

// Computed
const items = computed(() => store.items)
const loadingState = computed(() => store.loading.items)

const filteredItems = computed(() => {
  let result = [...items.value]

  // Filter out incomplete or invalid items (must have name, category, unit)
  result = result.filter(item => 
    item && 
    item.name && 
    item.name.trim() !== '' && 
    item.category &&  // category is now an ID
    item.unit &&
    item.unit.trim() !== '' &&
    item.id !== null &&
    item.id !== undefined
  )

  // Search filter (using debounced value)
  if (debouncedSearchQuery.value.trim()) {
    const query = debouncedSearchQuery.value.toLowerCase().trim()
    result = result.filter(item =>
      item.name.toLowerCase().includes(query)
    )
  }

  // Category filter (by ID now)
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

// Computed for displayed items (with show more functionality)
const displayedItems = computed(() => {
  return filteredItems.value.slice(0, itemsToShow.value)
})

const hasMoreItems = computed(() => {
  return filteredItems.value.length > itemsToShow.value
})

const showLessButton = computed(() => {
  return itemsToShow.value > 5
})

// Methods for show more/less
const showMore = () => {
  itemsToShow.value += 5
}

const showLess = () => {
  itemsToShow.value = 5
}

// Reset items to show when filters change
watch([debouncedSearchQuery, selectedCategory, selectedUnit], () => {
  itemsToShow.value = 5
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

const openQuickUsage = (item) => {
  selectedItem.value = item
  showUsageModal.value = true
}

const closeUsageModal = () => {
  showUsageModal.value = false
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

const handleQuickUsage = async (formData) => {
  movementLoading.value = true
  try {
    await store.addStockMovement(formData)
    toast.success('Usage tracked successfully')
    closeUsageModal()
    // Reload items to update stock levels
    await loadItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to track usage'
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

const formatCurrency = (value) => {
  if (!value) return 'KSh 0.00'
  // Format number with commas and add KSh prefix
  return 'KSh ' + new Intl.NumberFormat('en-KE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

// Lifecycle
onMounted(() => {
  loadItems()
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
</style>

