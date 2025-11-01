<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <!-- Page Header -->
      <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Requisitions</h1>
          <p class="text-gray-600 mt-1">Manage item requisition requests</p>
        </div>
        <div class="flex gap-2">
          <BaseButton
            v-if="selectedRequisitions.length > 0 && activeTab === 'pending'"
            variant="primary"
            @click="showBulkApproveConfirm = true"
            :disabled="bulkActionLoading"
          >
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Approve Selected ({{ selectedRequisitions.length }})
          </BaseButton>
          <BaseButton
            variant="secondary"
            @click="exportToCSV"
            :disabled="loading || filteredRequisitions.length === 0"
          >
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export CSV
          </BaseButton>
          <BaseButton variant="primary" @click="openCreateModal">
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Create Requisition
          </BaseButton>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <BaseCard>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Pending</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">
                {{ pendingCount }}
              </p>
            </div>
            <div class="p-3 bg-yellow-100 rounded-full">
              <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
        </BaseCard>

        <BaseCard>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Most Requested Item</p>
              <p class="text-sm font-semibold text-gray-900 mt-1 truncate">
                {{ mostRequestedItem?.name || 'N/A' }}
              </p>
              <p class="text-xs text-gray-500">
                {{ mostRequestedItem?.count || 0 }} requests
              </p>
            </div>
            <div class="p-3 bg-blue-100 rounded-full">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
        </BaseCard>

        <BaseCard>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Urgent (0 Stock)</p>
              <p class="text-2xl font-bold text-red-600 mt-1">
                {{ urgentCount }}
              </p>
            </div>
            <div class="p-3 bg-red-100 rounded-full">
              <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Tabs and Search -->
      <BaseCard class="mb-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Tabs -->
          <div class="flex border-b border-gray-200">
            <button
              v-for="tab in tabs"
              :key="tab.value"
              @click="activeTab = tab.value"
              :class="[
                'px-4 py-2 text-sm font-medium border-b-2 transition-colors',
                activeTab === tab.value
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.label }}
              <span v-if="tab.count !== undefined" class="ml-2 px-2 py-0.5 text-xs rounded-full"
                :class="activeTab === tab.value ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'">
                {{ tab.count }}
              </span>
            </button>
          </div>

          <!-- Search -->
          <div class="flex-1 max-w-md">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by item name or requester..."
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
          <BaseButton variant="primary" @click="loadRequisitions" class="mt-4">
            Try Again
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Empty State -->
      <BaseCard v-else-if="filteredRequisitions.length === 0">
        <div class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="mt-2 text-gray-500">No requisitions found</p>
          <BaseButton variant="primary" @click="openCreateModal" class="mt-4">
            Create First Requisition
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Requisitions Table -->
      <BaseCard v-else>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th v-if="activeTab === 'pending'" class="px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    :checked="allSelected"
                    @change="toggleSelectAll"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  @click="sortBy('date_requested')"
                >
                  <div class="flex items-center gap-2">
                    Date Requested
                    <svg v-if="sortField === 'date_requested'" class="w-4 h-4" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                    </svg>
                  </div>
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Item
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Quantity Requested
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Requested By
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date Processed
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="req in sortedRequisitions"
                :key="req.id"
                :class="[
                  'hover:bg-gray-50 transition-colors',
                  isUrgent(req) ? 'bg-red-50' : ''
                ]"
              >
                <td v-if="activeTab === 'pending'" class="px-6 py-4 whitespace-nowrap">
                  <input
                    type="checkbox"
                    :checked="selectedRequisitions.includes(req.id)"
                    @change="toggleSelection(req.id)"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(req.date_requested) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center gap-2">
                    <div>
                      <div class="text-sm font-medium text-gray-900">
                        {{ req.item_name || req.item?.name || 'Unknown' }}
                      </div>
                      <div class="text-xs text-gray-500">
                        <StockBadge
                          :current="getItemStock(req)"
                          :minimum="getItemMinStock(req)"
                          :show-percentage="false"
                        />
                      </div>
                    </div>
                    <span v-if="isUrgent(req)" class="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-800 rounded">
                      URGENT
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                  {{ req.quantity_requested }} {{ getItemUnit(req) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ req.requested_by }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="getStatusBadgeClass(req.status)"
                  >
                    {{ getStatusLabel(req.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ req.date_processed ? formatDate(req.date_processed) : '—' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex items-center justify-end gap-2">
                    <template v-if="req.status === 'pending'">
                      <BaseButton
                        variant="primary"
                        @click="confirmApprove(req)"
                        :disabled="actionLoading"
                        class="text-xs px-2 py-1"
                      >
                        Approve
                      </BaseButton>
                      <BaseButton
                        variant="danger"
                        @click="confirmReject(req)"
                        :disabled="actionLoading"
                        class="text-xs px-2 py-1"
                      >
                        Reject
                      </BaseButton>
                    </template>
                    <button
                      v-else
                      @click="viewDetails(req)"
                      class="text-blue-600 hover:text-blue-900"
                      title="View Details"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </BaseCard>

      <!-- Create Requisition Modal -->
      <BaseModal :show="showCreateModal" title="Create Requisition" @close="closeCreateModal">
        <RequisitionForm
          :loading="createLoading"
          @submit="handleCreateRequisition"
          @cancel="closeCreateModal"
        />
      </BaseModal>

      <!-- View Details Modal -->
      <BaseModal :show="showDetailsModal" title="Requisition Details" @close="closeDetailsModal">
        <div v-if="selectedRequisition" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium text-gray-500">Date Requested</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDate(selectedRequisition.date_requested) }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Status</label>
              <p class="mt-1">
                <span
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="getStatusBadgeClass(selectedRequisition.status)"
                >
                  {{ getStatusLabel(selectedRequisition.status) }}
                </span>
              </p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Item</label>
              <p class="mt-1 text-sm text-gray-900">
                {{ selectedRequisition.item_name || selectedRequisition.item?.name || 'Unknown' }}
              </p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Quantity Requested</label>
              <p class="mt-1 text-sm font-medium text-gray-900">
                {{ selectedRequisition.quantity_requested }} {{ getItemUnit(selectedRequisition) }}
              </p>
            </div>
            <div>
              <label class="text-sm font-medium text-gray-500">Requested By</label>
              <p class="mt-1 text-sm text-gray-900">{{ selectedRequisition.requested_by }}</p>
            </div>
            <div v-if="selectedRequisition.date_processed">
              <label class="text-sm font-medium text-gray-500">Date Processed</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDate(selectedRequisition.date_processed) }}</p>
            </div>
          </div>
          <div v-if="selectedRequisition.notes">
            <label class="text-sm font-medium text-gray-500">Notes</label>
            <p class="mt-1 text-sm text-gray-900 whitespace-pre-wrap">{{ selectedRequisition.notes }}</p>
          </div>
        </div>
      </BaseModal>

      <!-- Approval Confirmation -->
      <ConfirmDialog
        :show="showApproveConfirm"
        title="Approve Requisition"
        :message="`Are you sure you want to approve this requisition for ${approveRequisition?.quantity_requested} ${getItemUnit(approveRequisition)} of ${approveRequisition?.item_name || 'item'}?`"
        confirm-text="Approve"
        cancel-text="Cancel"
        variant="primary"
        @confirm="handleApprove"
        @cancel="cancelApprove"
      />

      <!-- Rejection Confirmation -->
      <ConfirmDialog
        :show="showRejectConfirm"
        title="Reject Requisition"
        :message="`Are you sure you want to reject this requisition for ${rejectRequisition?.quantity_requested} ${getItemUnit(rejectRequisition)} of ${rejectRequisition?.item_name || 'item'}?`"
        confirm-text="Reject"
        cancel-text="Cancel"
        variant="danger"
        @confirm="handleReject"
        @cancel="cancelReject"
      />

      <!-- Bulk Approve Confirmation -->
      <ConfirmDialog
        :show="showBulkApproveConfirm"
        title="Bulk Approve Requisitions"
        :message="`Are you sure you want to approve ${selectedRequisitions.length} requisition(s)?`"
        confirm-text="Approve All"
        cancel-text="Cancel"
        variant="primary"
        @confirm="handleBulkApprove"
        @cancel="showBulkApproveConfirm = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import { useDebounce } from '../composables/useDebounce'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import StockBadge from '../components/StockBadge.vue'
import RequisitionForm from '../components/RequisitionForm.vue'

const store = useInventoryStore()
const toast = useToast()

// State
const loading = ref(false)
const error = ref(null)
const createLoading = ref(false)
const actionLoading = ref(false)
const bulkActionLoading = ref(false)
const requisitions = ref([])
const searchQuery = ref('')
const debouncedSearchQuery = useDebounce(searchQuery, 300)
const activeTab = ref('all')
const sortField = ref('date_requested')
const sortDirection = ref('desc')
const selectedRequisitions = ref([])

// Modal states
const showCreateModal = ref(false)
const showDetailsModal = ref(false)
const showApproveConfirm = ref(false)
const showRejectConfirm = ref(false)
const showBulkApproveConfirm = ref(false)
const selectedRequisition = ref(null)
const approveRequisition = ref(null)
const rejectRequisition = ref(null)

// Tabs configuration
const tabs = computed(() => {
  const all = requisitions.value.length
  const pending = requisitions.value.filter(r => r.status === 'pending').length
  const approved = requisitions.value.filter(r => r.status === 'approved').length
  const rejected = requisitions.value.filter(r => r.status === 'rejected').length

  return [
    { value: 'all', label: 'All', count: all },
    { value: 'pending', label: 'Pending', count: pending },
    { value: 'approved', label: 'Approved', count: approved },
    { value: 'rejected', label: 'Rejected', count: rejected }
  ]
})

// Computed
const filteredRequisitions = computed(() => {
  let result = [...requisitions.value]

  // Filter by status tab
  if (activeTab.value !== 'all') {
    result = result.filter(r => r.status === activeTab.value)
  }

  // Search filter (using debounced value)
  if (debouncedSearchQuery.value.trim()) {
    const query = debouncedSearchQuery.value.toLowerCase().trim()
    result = result.filter(r => {
      const itemName = (r.item_name || r.item?.name || '').toLowerCase()
      const requestedBy = (r.requested_by || '').toLowerCase()
      return itemName.includes(query) || requestedBy.includes(query)
    })
  }

  return result
})

const sortedRequisitions = computed(() => {
  const result = [...filteredRequisitions.value]

  result.sort((a, b) => {
    let aVal = a[sortField.value]
    let bVal = b[sortField.value]

    if (sortField.value === 'date_requested' || sortField.value === 'date_processed') {
      aVal = new Date(aVal || 0)
      bVal = new Date(bVal || 0)
    } else if (typeof aVal === 'string') {
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

const pendingCount = computed(() => {
  return requisitions.value.filter(r => r.status === 'pending').length
})

const urgentCount = computed(() => {
  return requisitions.value.filter(r => {
    if (r.status !== 'pending') return false
    const item = store.itemById(r.item_id || r.item?.id)
    return item && item.current_stock === 0
  }).length
})

const mostRequestedItem = computed(() => {
  const itemCounts = {}
  requisitions.value.forEach(req => {
    const itemId = req.item_id || req.item?.id
    if (itemId) {
      if (!itemCounts[itemId]) {
        itemCounts[itemId] = { id: itemId, count: 0, name: req.item_name || req.item?.name }
      }
      itemCounts[itemId].count++
    }
  })

  const sorted = Object.values(itemCounts).sort((a, b) => b.count - a.count)
  return sorted[0] || null
})

const allSelected = computed(() => {
  const pending = filteredRequisitions.value.filter(r => r.status === 'pending')
  return pending.length > 0 && pending.every(r => selectedRequisitions.value.includes(r.id))
})

// Methods
const loadRequisitions = async () => {
  loading.value = true
  error.value = null
  try {
    await store.fetchRequisitions({ ordering: '-date_requested' })
    requisitions.value = store.requisitions
  } catch (err) {
    error.value = err.message || 'Failed to load requisitions'
    toast.error('Failed to load requisitions')
  } finally {
    loading.value = false
  }
}

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'desc'
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusLabel = (status) => {
  const labels = {
    pending: 'Pending',
    approved: 'Approved',
    rejected: 'Rejected'
  }
  return labels[status] || status
}

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getItemStock = (req) => {
  const item = store.itemById(req.item_id || req.item?.id)
  return item?.current_stock ?? 0
}

const getItemMinStock = (req) => {
  const item = store.itemById(req.item_id || req.item?.id)
  return item?.min_stock_level ?? 0
}

const getItemUnit = (req) => {
  if (!req) return ''
  const item = store.itemById(req.item_id || req.item?.id)
  return item?.unit || 'units'
}

const isUrgent = (req) => {
  if (req.status !== 'pending') return false
  const item = store.itemById(req.item_id || req.item?.id)
  return item && item.current_stock === 0
}

// Selection methods
const toggleSelection = (id) => {
  const index = selectedRequisitions.value.indexOf(id)
  if (index > -1) {
    selectedRequisitions.value.splice(index, 1)
  } else {
    selectedRequisitions.value.push(id)
  }
}

const toggleSelectAll = () => {
  const pending = filteredRequisitions.value.filter(r => r.status === 'pending')
  if (allSelected.value) {
    selectedRequisitions.value = selectedRequisitions.value.filter(
      id => !pending.some(r => r.id === id)
    )
  } else {
    pending.forEach(r => {
      if (!selectedRequisitions.value.includes(r.id)) {
        selectedRequisitions.value.push(r.id)
      }
    })
  }
}

// Modal handlers
const openCreateModal = () => {
  showCreateModal.value = true
}

const closeCreateModal = () => {
  showCreateModal.value = false
}

const handleCreateRequisition = async (formData) => {
  createLoading.value = true
  try {
    await store.createRequisition(formData)
    toast.success('Requisition created successfully')
    closeCreateModal()
    await loadRequisitions()
    // Reload items to update stock info
    await store.fetchItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to create requisition'
    toast.error(errorMessage)
  } finally {
    createLoading.value = false
  }
}

const viewDetails = (req) => {
  selectedRequisition.value = req
  showDetailsModal.value = true
}

const closeDetailsModal = () => {
  showDetailsModal.value = false
  selectedRequisition.value = null
}

const confirmApprove = (req) => {
  approveRequisition.value = req
  showApproveConfirm.value = true
}

const cancelApprove = () => {
  showApproveConfirm.value = false
  approveRequisition.value = null
}

const handleApprove = async () => {
  if (!approveRequisition.value) return

  actionLoading.value = true
  try {
    await store.approveRequisition(approveRequisition.value.id)
    toast.success('Requisition approved successfully')
    cancelApprove()
    await loadRequisitions()
    await store.fetchItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to approve requisition'
    toast.error(errorMessage)
    cancelApprove()
  } finally {
    actionLoading.value = false
  }
}

const confirmReject = (req) => {
  rejectRequisition.value = req
  showRejectConfirm.value = true
}

const cancelReject = () => {
  showRejectConfirm.value = false
  rejectRequisition.value = null
}

const handleReject = async () => {
  if (!rejectRequisition.value) return

  actionLoading.value = true
  try {
    await store.rejectRequisition(rejectRequisition.value.id)
    toast.success('Requisition rejected')
    cancelReject()
    await loadRequisitions()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to reject requisition'
    toast.error(errorMessage)
    cancelReject()
  } finally {
    actionLoading.value = false
  }
}

const handleBulkApprove = async () => {
  if (selectedRequisitions.value.length === 0) return

  bulkActionLoading.value = true
  try {
    const promises = selectedRequisitions.value.map(id => store.approveRequisition(id))
    await Promise.all(promises)
    toast.success(`${selectedRequisitions.value.length} requisition(s) approved successfully`)
    selectedRequisitions.value = []
    showBulkApproveConfirm.value = false
    await loadRequisitions()
    await store.fetchItems()
  } catch (err) {
    toast.error('Failed to approve some requisitions')
    console.error('Bulk approve error:', err)
  } finally {
    bulkActionLoading.value = false
  }
}

const exportToCSV = () => {
  if (filteredRequisitions.value.length === 0) {
    toast.warning('No requisitions to export')
    return
  }

  const headers = [
    'Date Requested',
    'Item',
    'Quantity Requested',
    'Requested By',
    'Status',
    'Date Processed'
  ]

  const rows = filteredRequisitions.value.map(req => [
    formatDate(req.date_requested),
    req.item_name || req.item?.name || 'Unknown',
    `${req.quantity_requested} ${getItemUnit(req)}`,
    req.requested_by,
    getStatusLabel(req.status),
    req.date_processed ? formatDate(req.date_processed) : ''
  ])

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `requisitions-${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  toast.success('CSV exported successfully')
}

// Watch tab changes to clear selections
watch(() => activeTab.value, () => {
  selectedRequisitions.value = []
})

// Lifecycle
onMounted(async () => {
  await loadRequisitions()
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

