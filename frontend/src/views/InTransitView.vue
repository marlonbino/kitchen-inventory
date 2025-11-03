<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-3 sm:p-4 md:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-2 bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">In Transit Orders</h1>
        <p class="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-300 font-medium">Approve and confirm your ordered items</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg overflow-hidden">
        <div class="p-6 space-y-3">
          <div v-for="n in 6" :key="n" class="h-16 bg-neutral-700/50 dark:bg-neutral-700/50 rounded animate-pulse"></div>
        </div>
      </div>

      <!-- Error State -->
      <BaseCard v-else-if="error">
        <div class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-2 text-red-600">{{ error }}</p>
          <BaseButton variant="primary" @click="loadDeliveries" class="mt-4">
            Try Again
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Empty State -->
      <BaseCard v-else-if="awaitingDeliveries.length === 0">
        <div class="text-center py-12">
          <div class="inline-flex p-4 bg-green-400 dark:bg-green-400 rounded-full mb-4">
            <svg class="h-12 w-12 text-black dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-lg font-semibold text-white dark:text-white">All clear!</p>
          <p class="mt-1 text-gray-300 dark:text-gray-300">No items awaiting delivery</p>
        </div>
      </BaseCard>

      <!-- Deliveries Table -->
      <div v-else class="hidden md:block">
        <div class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
          <div class="overflow-x-auto custom-scrollbar">
            <table class="min-w-full">
              <thead class="bg-neutral-800/50 dark:bg-neutral-800/50">
                <tr>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    DATE ORDERED
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    ITEM
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    QUANTITY
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    COST (KES)
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    REQUESTED BY
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    ASSIGNED TO
                  </th>
                  <th class="px-6 py-4 text-right text-xs font-bold text-white uppercase tracking-wider">
                    ACTION
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="req in awaitingDeliveries"
                  :key="req.id"
                  class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-all duration-200"
                >
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ formatDate(req.date_requested) }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <div class="text-sm font-semibold text-white dark:text-white">
                        {{ req.item_name || req.item?.name || 'Unknown' }}
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300 font-medium">
                      {{ req.quantity_requested }} {{ getItemUnit(req) }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm font-semibold text-gray-300 dark:text-gray-300">
                      {{ getReqCost(req) }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ req.requested_by }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ req.assigned_to || '-' }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap text-right">
                    <button
                      @click="handleConfirmDelivery(req)"
                      :disabled="confirming"
                      class="inline-flex items-center px-4 py-2 bg-green-500 hover:bg-green-600 disabled:bg-green-300 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-lg transition-colors duration-200"
                    >
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                      {{ confirming ? 'Confirming...' : 'Confirm' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Mobile Card View -->
      <div v-if="!loading && !error && awaitingDeliveries.length > 0" class="md:hidden space-y-4">
        <div
          v-for="req in awaitingDeliveries"
          :key="req.id"
          class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300 p-4"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-white dark:text-white">{{ req.item_name || req.item?.name || 'Unknown' }}</h3>
              <p class="text-sm text-gray-300 dark:text-gray-300 mt-1">{{ req.requested_by }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div>
              <span class="text-gray-400 dark:text-gray-400">Quantity:</span>
              <span class="ml-2 font-medium text-white dark:text-white">{{ req.quantity_requested }} {{ getItemUnit(req) }}</span>
            </div>
            <div>
              <span class="text-gray-400 dark:text-gray-400">Cost:</span>
              <span class="ml-2 font-semibold text-white dark:text-white">{{ getReqCost(req) }}</span>
            </div>
          </div>
          <div class="text-sm mb-4">
            <span class="text-gray-400 dark:text-gray-400">Date:</span>
            <span class="ml-2 font-medium text-white dark:text-white">{{ formatDate(req.date_requested) }}</span>
          </div>

          <div class="pt-3 border-t dark:border-neutral-700">
            <button
              @click="handleConfirmDelivery(req)"
              :disabled="confirming"
              class="w-full bg-green-500 hover:bg-green-600 disabled:bg-green-300 disabled:cursor-not-allowed text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 text-sm"
            >
              <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ confirming ? 'Confirming...' : 'Confirm Delivery' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'

const store = useInventoryStore()
const toast = useToast()

const loading = ref(false)
const error = ref(null)
const confirming = ref(false)

const awaitingDeliveries = computed(() => {
  return store.requisitions.filter(req => req.status === 'awaiting_delivery')
})

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

const getItemUnit = (req) => {
  if (!req) return ''
  const item = store.itemById(req.item_id || req.item?.id)
  return item?.unit || 'units'
}

const getReqCost = (req) => {
  if (!req) return '—'
  const item = store.itemById(req.item_id || req.item?.id)
  if (!item || !item.price_per_unit) return '—'
  const cost = parseFloat(item.price_per_unit) * req.quantity_requested
  return formatCurrency(cost)
}

const formatCurrency = (value) => {
  if (!value) return 'KSh 0.00'
  return 'KSh ' + new Intl.NumberFormat('en-KE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

const loadDeliveries = async () => {
  loading.value = true
  error.value = null
  try {
    await store.fetchRequisitions({ ordering: '-date_requested' })
  } catch (err) {
    error.value = err.message || 'Failed to load deliveries'
    toast.error('Failed to load deliveries')
  } finally {
    loading.value = false
  }
}

const handleConfirmDelivery = async (req) => {
  if (confirming.value) return
  
  confirming.value = true
  try {
    await store.confirmReceived(req.id, req.quantity_requested, '')
    toast.success('Delivery confirmed! Stock has been added.')
    await loadDeliveries()
    // Reload items to update stock
    await store.fetchItems()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to confirm delivery')
  } finally {
    confirming.value = false
  }
}

onMounted(() => {
  loadDeliveries()
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

