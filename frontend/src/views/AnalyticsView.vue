<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-3 sm:p-4 md:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Page Header -->
      <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Statistics</h1>
          <p class="text-gray-600 dark:text-gray-200 font-medium mt-1">Numbers and insights for planning</p>
        </div>
        <div class="flex gap-2">
          <BaseButton
            variant="secondary"
            @click="showReportModal = true"
            class="shadow-md"
          >
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generate Report
          </BaseButton>
          <BaseButton
            variant="primary"
            @click="printReport"
            class="shadow-md"
          >
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            Print Report
          </BaseButton>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-6">
        <div v-for="n in 3" :key="n" class="bg-white dark:bg-neutral-800 rounded-xl shadow-md p-6 animate-pulse">
          <div class="h-4 bg-gray-200 dark:bg-neutral-700 rounded w-3/4 mb-3"></div>
          <div class="h-32 bg-gray-200 dark:bg-neutral-700 rounded"></div>
        </div>
      </div>

      <!-- Analytics Content -->
      <div v-else class="space-y-6">
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <!-- Total Items Card -->
          <div class="stat-card group bg-gradient-to-br from-blue-900/20 to-neutral-900 dark:from-blue-900/20 dark:to-neutral-900 rounded-2xl p-6 border-2 border-blue-500/30 shadow-lg hover:shadow-2xl hover:border-blue-500/60 transition-all duration-300" style="animation-delay: 0s;">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <p class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Total Items</p>
                <p class="text-4xl sm:text-5xl font-extrabold text-white group-hover:scale-105 transition-transform duration-300">{{ stats.total_items }}</p>
                <p class="text-xs text-gray-500 mt-3">In inventory</p>
              </div>
              <div class="p-4 bg-transparent rounded-2xl group-hover:bg-blue-500/40 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 flex-shrink-0">
                <i class="fas fa-cubes text-4xl text-blue-400"></i>
              </div>
            </div>
          </div>

          <!-- Urgent Reorders Card -->
          <div class="stat-card group bg-gradient-to-br from-red-900/20 to-neutral-900 dark:from-red-900/20 dark:to-neutral-900 rounded-2xl p-6 border-2 border-red-500/30 shadow-lg hover:shadow-2xl hover:border-red-500/60 transition-all duration-300" style="animation-delay: 0.15s;">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <p class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Urgent Reorders</p>
                <div class="flex items-baseline gap-2">
                  <p class="text-4xl sm:text-5xl font-extrabold text-red-400 group-hover:scale-105 transition-transform duration-300">{{ stats.low_stock_count }}</p>
                  <span v-if="stats.low_stock_count > 0" class="px-2 py-1 bg-red-500 text-white text-xs font-bold rounded-full animate-pulse">!</span>
                </div>
                <p class="text-xs text-gray-500 mt-3">Need restocking</p>
              </div>
              <div class="p-4 bg-transparent rounded-2xl group-hover:bg-red-500/40 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 flex-shrink-0">
                <i class="fas fa-exclamation-triangle text-4xl text-red-400"></i>
              </div>
            </div>
          </div>

          <!-- Pending Approvals Card -->
          <div class="stat-card group bg-gradient-to-br from-yellow-900/20 to-neutral-900 dark:from-yellow-900/20 dark:to-neutral-900 rounded-2xl p-6 border-2 border-yellow-500/30 shadow-lg hover:shadow-2xl hover:border-yellow-500/60 transition-all duration-300" style="animation-delay: 0.3s;">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <p class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Pending Approvals</p>
                <p class="text-4xl sm:text-5xl font-extrabold text-yellow-400 group-hover:scale-105 transition-transform duration-300">{{ stats.pending_requisitions }}</p>
                <p class="text-xs text-gray-500 mt-3">Awaiting action</p>
              </div>
              <div class="p-4 bg-transparent rounded-2xl group-hover:bg-yellow-500/40 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 flex-shrink-0">
                <i class="fas fa-clipboard-check text-4xl text-yellow-400"></i>
              </div>
            </div>
          </div>

          <!-- Total Stock Value Card -->
          <div class="stat-card group bg-gradient-to-br from-green-900/20 to-neutral-900 dark:from-green-900/20 dark:to-neutral-900 rounded-2xl p-6 border-2 border-green-500/30 shadow-lg hover:shadow-2xl hover:border-green-500/60 transition-all duration-300" style="animation-delay: 0.45s;">
            <div class="flex flex-col gap-4">
              <div class="flex items-start justify-between">
                <div class="flex-1 overflow-hidden">
                  <p class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Stock Value</p>
                  <div class="group-hover:scale-105 transition-transform duration-300">
                    <p class="text-lg sm:text-xl font-bold text-green-400 mb-1">KSh</p>
                    <p class="text-lg sm:text-xl lg:text-2xl font-extrabold text-green-400 whitespace-nowrap leading-tight">{{ formatCurrency(stats.total_stock_value).replace('KSh ', '') }}</p>
                  </div>
                  <p class="text-xs text-gray-500 mt-3">Kenyan Shillings</p>
                </div>
                <div class="p-4 bg-transparent rounded-2xl group-hover:bg-green-500/40 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 flex-shrink-0">
                  <i class="fas fa-money-bill-wave text-4xl text-green-400"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
          <!-- Category Distribution -->
          <div class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl p-6 border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 bg-blue-500/20 rounded-lg">
                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 class="text-lg font-bold text-white">Items by Category</h3>
            </div>
            <div v-if="categoryData.length === 0" class="flex items-center justify-center h-64">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p class="text-gray-400">No category data available</p>
              </div>
            </div>
            <div v-else class="space-y-5">
              <div
                v-for="item in categoryData"
                :key="item.category"
                class="group"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-semibold text-gray-300 group-hover:text-white transition-colors">{{ item.category }}</span>
                  <div class="flex items-center gap-3">
                    <span class="text-sm font-bold text-white">{{ item.count }}</span>
                    <span class="text-xs font-medium text-gray-400">{{ item.percentage }}%</span>
                  </div>
                </div>
                <div class="w-full bg-neutral-700 rounded-full h-3 overflow-hidden">
                  <div
                    class="h-3 rounded-full transition-all duration-500 group-hover:brightness-110"
                    :style="{ width: item.percentage + '%', backgroundColor: item.color }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Low Stock Breakdown -->
          <div class="bg-gradient-to-br from-red-900/20 to-neutral-900 dark:from-red-900/20 dark:to-neutral-900 rounded-2xl p-6 border border-red-500/20 shadow-lg hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 bg-red-500/20 rounded-lg">
                <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <h3 class="text-lg font-bold text-white">Most Used Items</h3>
            </div>
            <div v-if="lowStockData.length === 0" class="flex items-center justify-center h-64">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto text-green-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-gray-400">All items are well stocked!</p>
              </div>
            </div>
            <div v-else class="space-y-3 max-h-80 overflow-y-auto custom-scrollbar pr-2">
              <div
                v-for="item in lowStockData"
                :key="item.id"
                class="group flex items-center justify-between p-4 bg-red-500/10 hover:bg-red-500/15 rounded-xl border border-red-500/20 hover:border-red-500/40 transition-all duration-200"
              >
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-bold text-white truncate group-hover:text-red-300 transition-colors">{{ item.name }}</p>
                  <p class="text-xs text-gray-400 mt-1.5">
                    <span class="font-semibold">Current:</span> {{ item.current_stock }} / 
                    <span class="font-semibold">Min:</span> {{ item.min_stock_level }} {{ item.unit }}
                  </p>
                </div>
                <div class="flex flex-col items-end ml-3">
                  <span class="text-lg font-extrabold text-red-400">{{ item.percentage }}%</span>
                  <span class="text-xs text-red-300 font-medium">stock</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl p-6 border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-purple-500/20 rounded-lg">
                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-lg font-bold text-white">Recent Activity</h3>
            </div>
            <router-link 
              to="/movements" 
              class="text-sm font-semibold text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-1 group"
            >
              View All
              <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>
          <div v-if="stats.recent_movements.length === 0" class="text-center py-12">
            <svg class="w-16 h-16 mx-auto text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p class="text-gray-400">No recent activity</p>
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="movement in stats.recent_movements"
              :key="movement.id"
              class="group flex items-center justify-between p-4 hover:bg-neutral-700/50 rounded-xl transition-all duration-200"
            >
              <div class="flex items-center gap-4">
                <div
                  class="w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200 group-hover:scale-110"
                  :class="getMovementColor(movement.movement_type)"
                >
                  <svg class="w-6 h-6" :class="getMovementIconColor(movement.movement_type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="movement.movement_type === 'receipt'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-bold text-white group-hover:text-gray-100 transition-colors">{{ movement.item_name || movement.item?.name || 'Unknown' }}</p>
                  <p class="text-xs text-gray-400 mt-1">{{ formatDate(movement.date) }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-base font-extrabold" :class="getMovementTextColor(movement.movement_type)">
                  {{ movement.movement_type === 'receipt' ? '+' : '-' }}{{ movement.quantity }} {{ movement.item?.unit || '' }}
                </p>
                <p class="text-xs text-gray-400 capitalize mt-1">{{ movement.movement_type }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Report Generation Modal -->
    <BaseModal
      :show="showReportModal"
      @close="showReportModal = false"
      title="Generate Custom Report"
    >
      <div class="space-y-4">
        <p class="text-gray-600 dark:text-gray-300">Configure your report settings:</p>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Report Period
          </label>
          <select
            v-model="reportPeriod"
            class="w-full px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white"
          >
            <option value="today">Today</option>
            <option value="week">Last 7 Days</option>
            <option value="month">Last 30 Days</option>
            <option value="quarter">Last 3 Months</option>
            <option value="year">Last 12 Months</option>
            <option value="all">All Time</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Purchase Request Status
          </label>
          <select
            v-model="reportStatus"
            class="w-full px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white"
          >
            <option value="all">All Requests</option>
            <option value="pending">Pending Approval</option>
            <option value="approved">Approved</option>
            <option value="awaiting_delivery">Awaiting Delivery</option>
            <option value="delivered">Delivered</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
          <p class="text-sm text-blue-800 dark:text-blue-200">
            <i class="fas fa-info-circle mr-2"></i>
            Report will include purchase request history based on your filter settings.
          </p>
        </div>

        <div class="flex justify-end gap-3 pt-4 border-t dark:border-neutral-700">
          <BaseButton
            variant="secondary"
            @click="showReportModal = false"
          >
            Cancel
          </BaseButton>
          <BaseButton
            variant="primary"
            @click="generateCustomReport"
          >
            <i class="fas fa-print mr-2"></i>
            Generate & Print
          </BaseButton>
        </div>
      </div>
    </BaseModal>

    <!-- Hidden Print Area -->
    <div id="print-report-area" style="display: none;">
      <div class="print-header">
        <h2>BITZ Kitchen System - Inventory Report</h2>
        <p class="report-date">Generated: {{ new Date().toLocaleString('en-KE') }}</p>
        <p class="report-period" v-if="reportPeriod !== 'all'">Period: {{ getPeriodLabel(reportPeriod) }}</p>
      </div>
      <div class="print-content" ref="printContent">
        <!-- Report content will be populated here -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import { getDashboardStats, getCategories } from '../services/api.js'
import bitzLogo from '../assets/bitz-logo.svg'
import bitzLogoReport from '../assets/bitz-logo.svg'

const store = useInventoryStore()
const toast = useToast()

const loading = ref(false)
const showReportModal = ref(false)
const reportPeriod = ref('month')
const reportStatus = ref('all')
const stats = ref({
  total_items: 0,
  low_stock_count: 0,
  pending_requisitions: 0,
  recent_movements: [],
  total_stock_value: 0
})
const requisitions = ref([])

// Computed data for charts
const categoryData = computed(() => {
  const categories = {}
  store.items.forEach(item => {
    const cat = item.category_name || 'Uncategorized'
    categories[cat] = (categories[cat] || 0) + 1
  })
  
  const total = Object.values(categories).reduce((sum, count) => sum + count, 0)
  
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4']
  
  return Object.entries(categories).map(([category, count], index) => ({
    category,
    count,
    percentage: total > 0 ? Math.round((count / total) * 100) : 0,
    color: colors[index % colors.length]
  })).sort((a, b) => b.count - a.count)
})

const lowStockData = computed(() => {
  return store.lowStockItems.map(item => ({
    ...item,
    percentage: item.min_stock_level > 0 
      ? Math.round((item.current_stock / item.min_stock_level) * 100) 
      : 0
  })).sort((a, b) => a.percentage - b.percentage)
})

const filteredRequisitions = computed(() => {
  const dateRange = getDateRange(reportPeriod.value)
  
  return requisitions.value.filter(req => {
    // Filter by status
    if (reportStatus.value !== 'all' && req.status !== reportStatus.value) {
      return false
    }
    
    // Filter by date range
    if (dateRange.start) {
      const reqDate = new Date(req.date_requested)
      if (reqDate < dateRange.start || reqDate > dateRange.end) {
        return false
      }
    }
    
    return true
  }).sort((a, b) => new Date(b.date_requested) - new Date(a.date_requested))
})

const requisitionStats = computed(() => {
  const total = filteredRequisitions.value.length
  const approved = filteredRequisitions.value.filter(r => r.status === 'awaiting_delivery' || r.status === 'delivered').length
  const rejected = filteredRequisitions.value.filter(r => r.status === 'rejected').length
  const pending = filteredRequisitions.value.filter(r => r.status === 'pending').length
  const totalCost = filteredRequisitions.value.reduce((sum, req) => {
    return sum + (parseFloat(req.estimated_cost) || 0)
  }, 0)
  
  return {
    total,
    approved,
    rejected,
    pending,
    totalCost
  }
})

// Methods
const loadAnalytics = async () => {
  loading.value = true
  try {
    const data = await getDashboardStats()
    stats.value = data
    await store.fetchRequisitions({ ordering: '-date_requested' })
    requisitions.value = store.requisitions
  } catch (err) {
    toast.error('Failed to load analytics data')
    console.error('Analytics error:', err)
  } finally {
    loading.value = false
  }
}

const getStatusLabel = (status) => {
  const labels = {
    pending: 'Pending Approval',
    approved: 'Approved',
    awaiting_delivery: 'Awaiting Delivery',
    delivered: 'Delivered',
    rejected: 'Rejected'
  }
  return labels[status] || status
}

const getStatusColor = (status) => {
  const colors = {
    pending: '#f59e0b',
    approved: '#3b82f6',
    awaiting_delivery: '#f97316',
    delivered: '#10b981',
    rejected: '#ef4444'
  }
  return colors[status] || '#6b7280'
}

const getItemUnit = (req) => {
  if (!req) return 'units'
  const item = store.itemById(req.item_id || req.item?.id)
  return item?.unit || 'units'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const formatCurrency = (value) => {
  if (!value) return 'KSh 0.00'
  // Format number with commas and add KSh prefix
  return 'KSh ' + new Intl.NumberFormat('en-KE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

const getMovementColor = (type) => {
  if (type === 'receipt') return 'bg-green-100 dark:bg-green-900/30'
  if (type === 'usage') return 'bg-orange-100 dark:bg-orange-900/30'
  return 'bg-red-100 dark:bg-red-900/30'
}

const getMovementIconColor = (type) => {
  if (type === 'receipt') return 'text-green-600 dark:text-green-400'
  if (type === 'usage') return 'text-orange-600 dark:text-orange-400'
  return 'text-red-600 dark:text-red-400'
}

const getMovementTextColor = (type) => {
  if (type === 'receipt') return 'text-green-600 dark:text-green-400'
  if (type === 'usage') return 'text-orange-600 dark:text-orange-400'
  return 'text-red-600 dark:text-red-400'
}

const getPeriodLabel = (period) => {
  const labels = {
    today: 'Today',
    week: 'Last 7 Days',
    month: 'Last 30 Days',
    quarter: 'Last 3 Months',
    year: 'Last 12 Months',
    all: 'All Time'
  }
  return labels[period] || period
}

const getDateRange = (period) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const ranges = {
    today: { start: today, end: new Date() },
    week: { start: new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000), end: new Date() },
    month: { start: new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000), end: new Date() },
    quarter: { start: new Date(today.getTime() - 90 * 24 * 60 * 60 * 1000), end: new Date() },
    year: { start: new Date(today.getTime() - 365 * 24 * 60 * 60 * 1000), end: new Date() },
    all: { start: null, end: new Date() }
  }
  
  return ranges[period] || ranges.month
}

const generateCustomReport = () => {
  showReportModal.value = false
  
  // Build report HTML
  const dateRange = getDateRange(reportPeriod.value)
  
  // BITZ Logo as base64 data URI for printing
  const logoBase64 = 'PHN2ZyB3aWR0aD0iMTg0IiBoZWlnaHQ9IjE4NCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgb3ZlcmZsb3c9ImhpZGRlbiI+PGRlZnM+PGltYWdlIHdpZHRoPSIxODQiIGhlaWdodD0iMTg0IiB4bGluazpocmVmPSJkYXRhOmltYWdlL2pwZWc7YmFzZTY0LC85ai80QUFRU2taSlJnQUJBUUVBbGdDV0FBRC8yd0JEQUFNQ0FnTUNBZ01EQXdNRUF3TUVCUWdGQlFRRUJRb0hCd1lJREFvTURBc0tDd3NORGhJUURRNFJEZ3NMRUJZUUVSTVVGUlVWREE4WEdCWVVHQklVRlJULzJ3QkRBUU1FQkFVRUJRa0ZCUWtVRFFzTkZCUVVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlFVRkJRVUZCUVVGQlQvd0FBUkNBQzRBTGdEQVNJQUFoRUJBeEVCLzhRQUh3QUFBUVVCQVFFQkFRRUFBQUFBQUFBQUFBRUNBd1FGQmdjSUNRb0wvOFFBdFJBQUFnRURBd0lFQXdVRkJBUUFBQUY5QVFJREFBUVJCUkloTVVFR0UxRmhCeUp4RkRLQmthRUlJMEt4d1JWUzBmQWtNMkp5Z2drS0ZoY1lHUm9sSmljb0tTbzBOVFkzT0RrNlEwUkZSa2RJU1VwVFZGVldWMWhaV21Oa1pXWm5hR2xxYzNSMWRuZDRlWHFEaElXR2g0aUppcEtUbEpXV2w1aVptcUtqcEtXbXA2aXBxckt6dExXMnQ3aTV1c0xEeE1YR3g4akp5dExUMU5YVzE5aloydUhpNCtUbDV1Zm82ZXJ4OHZQMDlmYjMrUG42LzhRQUh3RUFBd0VCQVFFQkFRRUJBUUFBQUFBQUFBRUNBd1FGQmdjSUNRb0wvOFFBdFJFQUFnRUNCQVFEQkFjRkJBUUFBUUozQUFFQ0F4RUVCU0V4QmhKQlVRZGhjUk1pTW9FSUZFS1JvYkhCQ1NNelV2QVZZbkxSQ2hZa05PRWw4UmNZR1JvbUp5Z3BLalUyTnpnNU9rTkVSVVpIU0VsS1UxUlZWbGRZV1ZwalpHVm1aMmhwYW5OMGRYWjNlSGw2Z29PRWhZYUhpSW1La3BPVWxaYVhtSm1hb3FPa3BhYW5xS21xc3JPMHRiYTN1TG02d3NQRXhjYkh5TW5LMHRQVTFkYlgyTm5hNHVQazVlYm42T25xOHZQMDlmYjMrUG42LzlvQURBTUJBQUlSQXhFQVB3RDlVNktLS0FDaWlpZ0Fvb29vQUtLS0tBQ2lpaWdBb29vb0FLS0tLQUNpaWlnQW9vb29BS0tLS0FDaWlpZ0Fvb29vQUtLS0tBQ2lpaWdBb29vb0FLS0tLQUNpaWlnQW9vb29BS0tLS0FDaWlpZ0Fvb29vQUtLS0tBQ2lpaWdBb29vb0FUTkdSNjE4L2ExKzBScmVtYTFxRmxIcGxpNlcxdzhLc3hmSkNzUms4KzFkeDhJUGlaZi9BQkVmVXhlMnR2YmZaZG0zeU04NXpuT2ZwVHRZRDBxaWlpa0FVVVVVQUZGRkZBQlJSUlFBVVVVVUFGSnVCNzBoUGF2emIrTm4vQlRmeDc4TVBpNzR1OEpXSGhUdzlkMldqYWc5bkRQY05QNWpxdU9XdzJNL1N1aWhocW1KazQwMXFoTnBINlNGbEhlblY4ZGZzT2Z0bmVLUDJwUEZYaXJUUEVHaGFUcEVXazJjTnpFK25HUXM1ZHlwRGJ5ZU1EdFgyTFVWYU02RTNUbnVDZDlVRkZGRlpEQ2lpaWdBb29vb0FLS0tLQVBpcnhhUCtLczFyL3I5bS84QVF6WHJuN012QjhRZGorNi9yWGtYaXc1OFc2MS8xK3pmK2htdlhmMlpUODNpRE9BUDNYSlAxclI3RW85NXBNZ1Z3WGlyNDFlR3ZDOHJ3TmNHL3VsT0dpdFBtMm4zYm9LNEs2L2Fia0xuN0xvUUNkakxQeWZ3QXFMTW85NnpTMTRUcC83VFkzZ1gyaHQ1ZmRyZWJKSDRFVjZONFQrSzNoM3hnVmlzN3Z5YnMvOEFMdGNEWTUrbnJSWURzS0tUTkxTQVRJOWFNajFyd2Y4QWJFL2FOdnYyWlBocmFlS05QMGFEVzU1OVFqcy9zOXhLWTFBWUU3c2o2VjhiTi93Vjg4VFpHZmg1cG5VRC9qK2svd0FLN3FXQ3IxNGUwcHJRbHlTM1AxQjYwWkZaM2h6VXpyUGg3VE5RWkJFMTNheFhCUlRrS1hVTmo4TTFhdkpUYldzOG9HVEdqUGoxd00xd2Ezc3lpWW5rVitESDdXL0g3VDN4T0gvVWJtL3BYMWZxSC9CWEx4Tlk2amVXeS9EN1RIRUU4a1FZM3Jna0t4WFBUMnI0ZStLUGp5ZjRvL0VieEg0dXViUkxDZldieHJ0N2FOaXl4bHV3SjYxOWRsV0RyWWVwS2RSYU5HVTJyV1B0WC9na0h4OFJQaUtlMzlsMjMvbzFxL1VYSXI4THYyVmYycHRSL1paMTNYOVUwN1FyYlhuMWUyanRuanVabWo4c0l4Ykl3T2M1cjZSLzRlK2VLUDhBb25tbC93RGdkSi9oWFBqOEJpSytJbE9tcm9JeVNWajlRTTBaRmZsODMvQlgzeEtxa3Q4UGRLR1BXK2svd3JyL0FBTC9BTUZIdmk3OFRwaEg0VitDWDl0anZOYnpTK1N2MWtJQ2o4Njg2V1dZbUt2SkpmTkZjeVoraVJJRkdSNjE4dWFCOGVmakhkSWtuaVB3MTRIOEpvM1dLNDFtUzVtWDZwRXA1L0d1NTBuOW9LQzNYL2ljVDIxeElPbzAyMmsyL2dYUDlLOCtkT1VIWmxIdFdjMHRlVEQ5cEh3M2svNkpxSC9mc2Y0MGY4TkkrRy8rZlcvL0FPL1kvd0FhaXpHZXMwVnduZ3o0djZQNDQxZHRPc1lMcU9jUm1YTXlBREEvR2lrQjh4K0svd0RrYk5iL0FPdjJiLzBNMHpUL0FCRHFPbGFmZVdWbmRQYlc5NFY4OFI4TTRIUVo2Z2M5cWs4V0RIaXpXLzhBcjltLzlETlo5cmJTM3R6RmJ3SVpKcFdDSWdITEVuZ1ZxU050N2VXNm1TS0NKNXBwRGhVakJabU5kM3BYd004WDZsQ0pmc0tXaXNNZ1hNd1Z2eTZpdmNmaGg4TWJMd0xweVN5UnBQckVxNW11R0dTdWY0VjlBUDFydXdNVlBOMkdqNUY4US9DWHhUNGJoYWU2MDB5MjZqTFMyekNRRDY0NXJrRVlvNGRXS3VweUdVNElQMXI3cEl5TVY0bDhiUGhOQTluUDRoMGFBUlhFZnozVnZHdnl5TDNjRDFGSE5mY0dVdmhGOGFaMnVZTkU4UVRHUlh3bHRmT2VRZXl2L1ExN3lwem5tdmhiTzRaSDFHRFgxTDhFZkd6K0xQQ2dodW4zNmhZRVFTdDNkZjRXL0xqOEtUUUkrYlArQ3NYL0FDYnhwUDhBMkhZUC9RV3I4bEdKeXZQY2Z6cjlhdjhBZ3JIL0FNbTc2Ui8ySFlQL0FFRjYvSlZ2NFQvdEQrZGZaNVQvQUxtL21aUytJL29tOEJEL0FJb2J3Ny8yRHJiL0FORkxXcnFNVFQyVnhHZ3k3eE1xajNJSUZaWGdQL2tSdkR2L0FHRHJiLzBVdGJ1SytMbGZtZGpZL0dqVmYrQ2IzeDN1dFgxQ2VMdzdwN1JUWE1zaUU2bkdNcXpramp0d2ErYmZHZmhEVS9oLzRzMWJ3MXJVU1FhdHBkdzF0ZFJSdUhWSkIxQVljSDhLL29veHpYNGMvSHY0ZStJZmlmOEF0Zy9FYlFmREdsemF2cWN1dHpFeFJEQ3hweGw1SDZJbzdzMksrdXk3SDFNVEp4cTJza1pUamM0cjRLL3MvZU52MmdkUzFPdzhFNmZCcU0rblJKUGNyUGNMQ0ZWaVZCRzdyelhyVnY4QThFNnZpeFlYOEMrSm0wWHd2cGpIOTVmWE4rc3hVZjdNYWZNNTlBSytrUDJZdmhsL3d5bFk2eGNXZXNSNjc0djFxM1NDK25oWC9Rck5VSllKRjNrYkpQekhBcjBLRzExL3gvcWp5cEhkNnplTWZtY0F0dDlzOUZGYytKeldwR280MG11VVNob2VTL0R2OW12NFhmQzhSVEpveitPZGJUbiswL0VRL3dCSFZ2V08xVTdmeFltdlVyenhKcU43YmkyZTZNTm1nd2xwYXFJWUVIb0VUQzRyMHp3OSt6bHJGOEZrMWE5aDA2TWptS0llWklQYjByMFBSL2dCNFYwMEtiaUtiVVpCMWE0aytVLzhCRmVEVnJ6ck84M2N0UnNmTHE0Qnd1Q2ZRYzFiaDB1K3V2OEFVMmR6TG4rNUV4L3BYMlRwL2cvUTlLVUxhYVRad0FkQ3NLNS9PdEIyZ3NZSGtieTRJb3h1WnNCUW9IZXNlWVo4V1RlSGRXdFlIbm0wdThpaFVibWtraEtxQjZra1ZuOVBhdlRQaTk4VjVQR04yK21hYkt5YUxDMkN3SkJ1R0hjK3c3Q3VLOEtlRjcveGpyY09tMkNicFgrWjVQNFkxN3NhcS9jRHYvMmRMYWFUeHRjenJHelF4MnJLOGdIQ2trWUJvcjNid1o0T3NmQldpUmFkWXJ3UG1rbEkrYVYrN0dpczJVZkpQaTMvQUpHelcvOEFyOW0vOUROZHgrejdvQ2F0NDBrdlpWM1I2ZkY1Z0I2Ynp3UDZtdUk4WUlZL0YrdHF3d1JleS84QW9acjFuOW1WMDgveEF2OEFIaUkvaDgxVzlFU2ozb0RGTFJSV1pRVkhORWs4YlJ5THZSd1ZaVDBJTlNVVUFmRnZqVFJmK0VkOFc2cnBvR0k3ZWRnbis2ZVIrbGRyK3oxcXJXSGpzMnU3RWQ1YnVwR2U2OGlzcjQydWpmRXpWZ21NQVI1eC9lMmpOSjhGRUwvRXJTZHZVYnlmcHROYVBZV3h6SC9CV1A4QTVOMjBqL3NPd2Y4QW9MMStTcC9oL3dCNGZ6cjlhdjhBZ3JIL0FNbTc2Ui8ySFlQL0FFRjYvSlZ2NFQvdEQrZGZZWlYvdWIrWmxMNGoraWJ3SC95STNoMy9BTEIxdC82S1d0M3BXRjREL3dDUkc4Ty85ZzYyL3dEUlMxRDQ0OGRhZDRHMGxydTlmZEsyUkRicWZubGIwQTlQZXZqWmJzMkwzaVh4UHAvaFBUSkwvVXJoWUlFSEEvaWMraWp1YStLdkcvalB3dDRPYnhKcnNVTnA0VDB6Vjd0NzNVWjJQNys4bFA4QXowYnEzYkNEZ1Y2VnB1bCtJL2p0NGxhNnVYTUdtd3RocFA4QWxsQ3Y5MUIzYXZ5Ly9hMjFPL2wrUHZqTFJiaS91THJUOUYxRjdPeWlrYjVZMFVESEE0em5QTmVsZ01NOFROd3ZidVJJKzZmMlBmaUg0Yy9hUStJM2lqVEYwMjQvc2ZRN1NLNGlsbWZZMXk3T1ZPNUJ5RkFIZm5tdnU3VHRLczlJdGt0N0sxaXRZRkdBa1NCUVB5cjh3LzhBZ2tGL3lVWDRpLzhBWUx0di9SclYrbzFaWTZsR2pYZE9PeUhGM1Z4Tm85S1dpa0p3TTF3RkRaSEVZM00yMEFFNVBRVjg1ZkdYNHRIeEJOSm9Xa1NrYWJHMjJlNFUvd0N2YjBCL3UvenJUK05YeGQrMUdidy9vazJJeDhsM2RJZnZmN0NuK1pyeGV6czU3KzZodGJhSnBybVk3RWlRY2tudFZKZFJNbjBYUmJ2WDlUZzArd2hNMXpNUXFxdlFlNTloWDFoOE92QUZwNEIwVVcwV0pyeVhEWE56am1SdlQ2RHRXZDhLZmhqYitCTkw4MllMTHJFNmd6eWorQWYzRjlCWGZEcFEzY0xCUlMwVkl6NVIrTjJoUG92eEN2bjJrUTNvRnpHZXh6dzM2aXJId0s4U1I2QjQ0amduWUpCcUVadHl4UFJzNVg5ZUs5ZytOZmdCL0dYaHY3UmFLRzFPeHpKRU1jeUxqNWsvcUsrWEZaNFpGWlM4TWlOa0hveWtmeU5XbmRhaVI5MFV0ZVYvQ240eFdmaVd6aDA3VjUwdGRYaVVLSGtPRnVCNmcrdnFLOVRCeU0xQXhhZ3ZMeUt4dDViaVp3a01TRjNZOWdCa21uVFR4d1F0Sks2eHhxTXM3bkFBOXpYejc4WnZpOUhyY0VtaGFKUHZzeWNYTjJuQWwvMkY5dlUwYmlaNWQ0bzFwdkVmaVBVdFNiL2w2bmFSYzlsN1Y2Vit6am9UM2ZpZTkxUmxQbFdrUGxxeDZiMjdmbFhsRm5aVFg5M0JhMjBabHVKbUNSeHFNa2sxOWQvRGJ3Wkg0SDhMMjlodzF5MzcyNGtIOFVoNi9nT240Vm85Z1I4bi93REJXSC9rM2JTZit3N0Ivd0Nndlg1S3QyLzNoL092MXIvNEt4LzhtNzZUL3dCaDJELzBGNi9PTDRBL0JHLytOdmpEN0dKR3NOQTA4TGNhcnFlM0lnaXp3aStzajlGSDQ5cSt1eXljWVlKeWs5TlRLWHhIN2FEeHhZZUJQaGJvRjdlTnZrYlRyZFlMZFQ4MHIrVXZBOXZVMTQzNGUwUFcvamg0dWx2TlFsZExPTS92cEYrNUNuYU5CNmtmNDF6alM2bDhRdkVPbTZmYmwyQ29sblp3TWNpR0pWQUdmZmFNazE5VytEdkN0cDROMEszMHl6VEN4akx5SHJJL2RqWHlNcks1c1hkRjBhejBIVExld3NJRnQ3V0ZkcUlvL1UrcDk2L0NYOXJiL2s1MzRuZjlodWIrbGZ2T2V0Zmd4KzF2eCswOThUaC8xRzVqL0t2Y3lUK05MME01YkgxSC93QUVndjhBa29ueEZQOEExQzdiL3dCR3RYNmpWK1VIL0JKZnhWWWFQOFp2Rm1qWFV5eFhlcmFTaHRWWTQ4eG9wTXNvOVRnNXg3VityMjcyTmNtYTZZdVZ4dzJETmVLZkd2NHV0cHlUYUJvc3crMU1OdDFkSWY4QVZBL3dLZjczcjZWb2ZHWDR1TDRiaGZSOUprRGFyS3VKWmw2VzZuLzJZL3BYemlXSmRuWWxwSE9TekhKTEhyOWE4eElvRVJwSFdPTkdlUmlBcUx5ek1mYjFOZlN2d2ErRksrRXJaZFcxT01QckU2NVZEMHQxUFlmN1hyV1I4RS9oTUxDT0x4RHJFUUYwM3pXdHM0LzFTbm81OS9UMHIydkk5UlNZa0FHS1dreVBVVVpIcUtReGFLYVhBNzBVQmNVak5lUC9BQlQrQ0NlSUo1dFcwTFpiNmczelMyemNKT2ZVSHMzODY5aHBNMERQaDdWTkt2Tkd2R3R0UXRKYk80US9jbFVnL2dlNDl4VzFwZnhHOFQ2UENJYlRXcnRJZ01CR2ZjQjlNMTljYXJvT242N0I1T28yVUY1SDJXWkEyUHA2VnhsMThCdkIxMUlYL3MrU0hQOEFERk13QXFyaXNmTit0ZU1OYzhRamJxV3FYTjBuOXg1Q0YvSVZEb0hodlUvRkY0dHRwZG5KZHlIajVCaFYrcmRCWDAzWWZBL3dmcDcrWi9aZjJnam9MaVJuSDVWMmVuNmRhYVpiaUN6dDRyV0VkRWhRS3Y1Q2szMkN4d1B3dCtFRnI0SVVYMTR5WG1zT3VQTUErV0Vkd3Y4QWpYcEFBRkE2VVpwWHZ1TStRdjhBZ3BUNEsxZjRpL0NQd3g0YzBPM056cWVvZUlyZUtKZWlvTnJiblk5bFVaSlBvSzg0OEIrQXRJK0ZmZzJ6OEthRmg3UzFiemJxOUs3WHZya2o1NTI5dW9VZGhYM2I0bThMMlhpelRtc3I1WE1ESEpNYmJXL0E5Um11TVA3UGZoQmdRWUxyQi82ZURYVjlZbDdGVVZzaWJhM01IOW5qd1VMTFRwdkVWekhpZTYvZFcyNGNySDNQNG4rVmUwQVlxdnB1bndhVllXOW5iSUk0SUVFYUtPd0ZXTTF6UFVZSHZYNHhmOEZGZmd4cW53MC9hQzFyeEMxcklmRDNpZVFYMXJlaFNZL05LanpJeWVnWUVaeDZHdjJkeldMNHM4SGFKNDUwV2JTUEVPbFdlczZaTU1QYTNzUWtRKytEL091M0I0cDRTcnoydWhOWFIvUEZwT3IzMmc2bGJhanBsN1BwOS9iT0pJYnExa0tTUnNPNnNPUlgxMyt6dDhVUGp4OFVkVmoxRFVmaVo0amc4SzJUZ1NQOW81dW5IL0xOZU9SNm44SysxTmIvQU9DYWZ3STFxOWU0WHc3ZWFjR2JjWWJHL2tqaitnQnppdlQ5RS9aaDhCK0c5SXRkTDAzVDVyU3h0a0VjVVVjNUFVRCt2Y212WHhlWjBLc1BkaGVYbWlWRm56ak5OSmRUeVR6TzBzMHJGbmtZNUxIdWM5NlpYMC8vQU1NK2VFVC9BTXNib2Y4QWJ3YVArR2UvQ1A4QXp4dXYvQWcxODdkRjJQbWthcGZEL2wrdXYrLzdmNDB2OXFYMy9QOEFYWC9mNXY4QUd2cFlmcytlRVIveXd1di9BQUpQK0ZIL0FBejU0Ui81NFhYL0FJRW1sZEJZK2FmN1V2OEEvbit1disvemY0MGYycGYvQVBQOWRmOEFmNXY4YStsditHZlBDUDhBend1di9BazBmOE0rZUVmK2VGMS80RW1pNkN4OC9lRTlTdlg4VmFPclhseVZhOGlCQm1ia2J4a2RhSytoN0w0RWVGZE92cmU3aGd1Uk5CSXNpRnJna1pCeVA1VVVYUVdQUmFyWFduVzE2d2FlSVNFZENTYXMwVkl6UC9zR3cvNTlsL00vNDBIUXRQSC9BQzdMK1oveHJRcnl6NHZYbHhiZU5QaHlrTThzVWN1cU1zaUk1QWNiT2pEdUtBUFFqb2VuWU9iZE1mN3gvd0FhRjBMVGowdGtJOWlmOGE4aitNSGgyeDBqWHZCWDJSSllQN1ExdFk3clpPLzcxU01sVDgzU3ZYZEYwT3owQzJhM3NZakRDV0xiUzVibjhTYUFBNkRwNEgvSHN2NW4vR2tYUTlQUEl0MFAwSi94cnpDenY3ajRqZkYzeEJwRjdkVHdhSDRmU05Wc1lKREdMaVZ1cnlFY2xSMkZkVHF0am9YdzF0TlI4VXNibTNndDdZK2JBazdORzNwaENTTnhQR2ZlZ0RwLzdCc1ArZlpmelA4QWpSL1lOaC96N0wrWi93QWE0TzgrS3Q5b1dsYUhyV3Q2TXRscEdxU3h4WlNiZkxiZVo5d3VNWTU3NDZVeTcrSit1WEhpN3hKb1dqNkZiM0xhTEVzenozRnlVRGdydXdBQjFOQUhmLzJEWWY4QVBzdjVuL0dnYURZRC9sMlg4ei9qWG5FbngwdG44TWVGOVZqczF0aHJzendlWmVTYllMVmxCenZjRG9TTUN0ZTQrSk56cHVwZUViRzcwK0I1dGVsa2lNbHJjaVNPTGFNaGcyUG1CR0tBT3VrMGZUNGxaM2dSVVVaSllrQUQxNjFGWmFmcEdvd0pQYXJCY1FPTXJKRSs1VytoQnJsSi9IUjF6V1BISGh3MmZrLzJUWTd2dE8vUG1iNHlmdTlzVjVuNFE4VGExNGIrR0h3dGcwZDRZazFDOSt6emh4OTlkekhhZU9CN2ptZ0QzdzZKcDI3YjluVGQxeGs1L25UdjdBMC8vbjJYOHovalhEdzZyWnQ4YTIwNlRUZHVxTG80bWE5U2R0dTNkZ3BzNmZqMXJuby9qbnJVbmhYVVBFcStHNGY3SDA2OGEybnpkSHpXVU50TElNWTR5T3RBSHJQOWcySC9BRDdMK1oveG8vc0d3LzU5bC9NLzQxeDk5OFRaWlBFeDBUU2RPRnpPbW1EVkpKYnFieWtDTjkxUndTU2Z5RmEvdzg4WmY4Sjc0VnRkYUZ1TFZaMllDSU1XSTJrZzVPQm5rVUFiQjBMVHdmOEFqMlg4ei9qUy93QmcySC9Qc3Y1bi9Hdk80N3k0L3dDR2pKYll6eS9aaG9RY1E3enMzYit1UFgzcTM4US9GV3VhTjQ3OEZhYnBza1NXdXBYRWlUcEovd0F0TnFFNEp4d1BwUUIzRGFIcDZqSnQxQStwL3dBYWl0ZE4wbTlqRXR1a004Uk9BOFQ3aG52eURYR3kvRVcvMXZYdkVXajZIcFVkNE5HaUMzZHhOTVVWcFNwUGxvTWNrZXBxbit6VXhiNFYyYk1wUmpkWEJLazVJUG1IaWdEMGFQUmJLRnc2VzZxdzVCeWVLS3U1elJRQXRGRkZBQlhLZU1mQXllTE5hOE9hZzkyMXVkR3VtdWdnWFBtRXJqQjlLNnVpZ0RrdkcvZ2FQeG5lZUg3bHJ0clp0SXZsdlZDcmtTRWZ3bjBycTErbUtkUlFCdzJzL0RxUWVMMjhVYUJxUDlrNnROR0lMdEhqOHlDNlFINWR5OWlPeEZUNnQ0TXZmRitrNm5wbmlIVUlialRyeUF3L1o3T0xac09jNzl4Sk9SaXV5cEtBUE9MejRWWFd1YVhvbWs2MXJKdnRLMHVTT1h5bzRBajNCai8xZm1Obm9PK090YXVtL0QxTk44V2VKOWJGNnp2cmtTUk5DVUdJZHFsYzU3OWE3TEE5S1dnRHpyUmZoaGRlSHZCK2wrSDdQVkxlZTB0V2xNNlh0a3NxWEFja2dGVDB3VDJyTmorQmNXbTZSNGRoMHpWNWJXLzBXOGt2SWJpU01Pak5KeTY3TThMNkFkSzlYb29BOC8wRDRaVGFYcmZpblZyelZ2dHQzcjBLd3loWVFpeEFLVkcwWjlEV2F2d1hhMThJK0Z0SXROV0tYWGgrNkYzQmN5UWdySWNuaGx6MDVyMUhBb3hRQnlFSGdQeS9pRi93bGt0Nlh1VzA0V0wyNnBoVDgyZHdQWDhLd292Z3hIRjhPTmE4SmYycElVMUs0a3VEYytXTXB1Y05nRDhLOU14UmlnRHdyeExwb3UvaWZiMk05NWE2WkJwV2pKQkhMcWtBZUs4RGZlMmNqcHRHUms5ZWxkMThJdFkxRFYvRFVvdnJDM3M0N1c1ZTJ0WHRJakZEUEN2M1pFVTlBYTdlVzJobng1c1NTWTZiMUJ4VWdVS0FBQUFCZ0FDbmNEaDlTK0g5M0w0L2J4WHArcUphWFRXUXNqQk5CNWliUTJjOVJ6VFBFZncvMUR4RGVlRzlTZlY0NDlXMGE0ZVpaQmIvQUxxVU1NRUZjOGNkODEzZEZJRHoxZmhqZDZicit1YW5vMnRmMmVOYlVHOGhlQVNBU1lJOHlQbmc4KzlOOFA4QXd5MVB3bDRMc2RDMGZ4SkpheVc5MmJpUzdhM1YybFF0bGtJUFRQclhvdEpnVUFJbjUwVTZpZ0Fvb29vQUtLS0tBQ2lpaWdBb29vb0FLS0tLQUNpaWlnQW9vb29BS0tLS0FDaWlpZ0Fvb29vQUtLS0tBQ2lpaWdBb29vb0FLS0tLQUNpaWlnQW9vb29BS0tLS0FDaWlpZ0Fvb29vQUtLS0tBQ2lpaWdBb29vb0FLS0tLQUNpaWlnQW9vb29BS0tLS0FDaWlpZ0Fvb29vQUtLS0tBQ2lpaWdnRC8yUT09IiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJub25lIiBpZD0iaW1nMCI+PC9pbWFnZT48Y2xpcFBhdGggaWQ9ImNsaXAxIj48cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTEyMTc2MSIgaGVpZ2h0PSIxMTIxNzYxIi8+PC9jbGlwUGF0aD48L2RlZnM+PGc+PGcgdHJhbnNmb3JtPSJzY2FsZSgwLjAwMDE2NDAyOCAwLjAwMDE2NDAyOCkiPjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMSkiPjx1c2Ugd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgeGxpbms6aHJlZj0iI2ltZzAiIHRyYW5zZm9ybT0ic2NhbGUoNjA5Ni41MyA2MDk2LjUzKSI+PC91c2U+PC9nPjwvZz48L2c+PC9zdmc+'
  
  const reportHtml = `
    <div style="font-family: 'Roboto', Arial, sans-serif; padding: 20px;">
      <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px; border-bottom: 3px solid #3b82f6; padding-bottom: 15px;">
        <img src="${bitzLogo}" alt="BITZ Logo" style="height: 50px; width: auto; flex-shrink: 0;">
        <div>
          <h1 style="color: #1f2937; margin: 0 0 5px 0; font-size: 28px; font-weight: bold;">BITZ Kitchen System</h1>
          <p style="color: #6b7280; margin: 0; font-size: 14px; font-weight: 500;">Inventory Report</p>
        </div>
      </div>
      
      <div style="margin-bottom: 30px;">
        <p><strong>Generated:</strong> ${new Date().toLocaleString('en-KE')}</p>
        <p><strong>Period:</strong> ${getPeriodLabel(reportPeriod.value)}</p>
        ${dateRange.start ? `<p><strong>Date Range:</strong> ${dateRange.start.toLocaleDateString('en-KE')} - ${dateRange.end.toLocaleDateString('en-KE')}</p>` : ''}
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
        <div style="background: #eff6ff; padding: 15px; border-radius: 8px;">
          <h3 style="color: #3b82f6; margin: 0 0 10px 0;">Total Items</h3>
          <p style="font-size: 28px; font-weight: bold; margin: 0;">${stats.value.total_items}</p>
        </div>
        
        <div style="background: #fef2f2; padding: 15px; border-radius: 8px;">
          <h3 style="color: #ef4444; margin: 0 0 10px 0;">Urgent Reorders</h3>
          <p style="font-size: 28px; font-weight: bold; margin: 0;">${stats.value.low_stock_count}</p>
        </div>
        
        <div style="background: #fffbeb; padding: 15px; border-radius: 8px;">
          <h3 style="color: #f59e0b; margin: 0 0 10px 0;">Pending Approvals</h3>
          <p style="font-size: 28px; font-weight: bold; margin: 0;">${stats.value.pending_requisitions}</p>
        </div>
        
        <div style="background: #f0fdf4; padding: 15px; border-radius: 8px;">
          <h3 style="color: #10b981; margin: 0 0 10px 0;">Total Stock Value</h3>
          <p style="font-size: 24px; font-weight: bold; margin: 0;">${formatCurrency(stats.value.total_stock_value)}</p>
        </div>
      </div>
      
      <div style="margin-bottom: 30px;">
        <h3 style="color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">Items by Category</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
          <thead>
            <tr style="background: #f3f4f6;">
              <th style="padding: 12px; text-align: left; border-bottom: 2px solid #d1d5db;">Category</th>
              <th style="padding: 12px; text-align: right; border-bottom: 2px solid #d1d5db;">Count</th>
              <th style="padding: 12px; text-align: right; border-bottom: 2px solid #d1d5db;">Percentage</th>
            </tr>
          </thead>
          <tbody>
            ${categoryData.value.map(item => `
              <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 10px;">${item.category}</td>
                <td style="padding: 10px; text-align: right;">${item.count}</td>
                <td style="padding: 10px; text-align: right;">${item.percentage}%</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      
      ${lowStockData.value.length > 0 ? `
      <div style="margin-bottom: 30px;">
        <h3 style="color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">Most Used Items (Low Stock)</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
          <thead>
            <tr style="background: #fee2e2;">
              <th style="padding: 12px; text-align: left; border-bottom: 2px solid #fecaca;">Item Name</th>
              <th style="padding: 12px; text-align: right; border-bottom: 2px solid #fecaca;">Current Stock</th>
              <th style="padding: 12px; text-align: right; border-bottom: 2px solid #fecaca;">Minimum Level</th>
              <th style="padding: 12px; text-align: right; border-bottom: 2px solid #fecaca;">Status</th>
            </tr>
          </thead>
          <tbody>
            ${lowStockData.value.map(item => `
              <tr style="border-bottom: 1px solid #fee2e2;">
                <td style="padding: 10px;">${item.name}</td>
                <td style="padding: 10px; text-align: right;">${item.current_stock} ${item.unit}</td>
                <td style="padding: 10px; text-align: right;">${item.min_stock_level} ${item.unit}</td>
                <td style="padding: 10px; text-align: right; color: #dc2626; font-weight: bold;">${item.percentage}%</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      ` : ''}
      
      <div style="margin-bottom: 30px;">
        <h3 style="color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">Purchase Request History</h3>
        <div style="background: #f9fafb; padding: 15px; border-radius: 8px; margin-top: 15px; margin-bottom: 15px;">
          <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px;">
            <div>
              <p style="color: #6b7280; font-size: 12px; margin: 0 0 5px 0;">Total Requests</p>
              <p style="font-size: 24px; font-weight: bold; color: #1f2937; margin: 0;">${requisitionStats.value.total}</p>
            </div>
            <div>
              <p style="color: #10b981; font-size: 12px; margin: 0 0 5px 0;">Approved</p>
              <p style="font-size: 24px; font-weight: bold; color: #10b981; margin: 0;">${requisitionStats.value.approved}</p>
            </div>
            <div>
              <p style="color: #ef4444; font-size: 12px; margin: 0 0 5px 0;">Rejected</p>
              <p style="font-size: 24px; font-weight: bold; color: #ef4444; margin: 0;">${requisitionStats.value.rejected}</p>
            </div>
            <div>
              <p style="color: #f59e0b; font-size: 12px; margin: 0 0 5px 0;">Pending</p>
              <p style="font-size: 24px; font-weight: bold; color: #f59e0b; margin: 0;">${requisitionStats.value.pending}</p>
            </div>
            <div>
              <p style="color: #059669; font-size: 12px; margin: 0 0 5px 0;">Total Cost</p>
              <p style="font-size: 20px; font-weight: bold; color: #059669; margin: 0;">${formatCurrency(requisitionStats.value.totalCost)}</p>
            </div>
          </div>
        </div>
        ${filteredRequisitions.value.length > 0 ? `
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px;">
          <thead>
            <tr style="background: #f3f4f6;">
              <th style="padding: 10px; text-align: left; border-bottom: 2px solid #d1d5db;">Date</th>
              <th style="padding: 10px; text-align: left; border-bottom: 2px solid #d1d5db;">Item</th>
              <th style="padding: 10px; text-align: right; border-bottom: 2px solid #d1d5db;">Qty</th>
              <th style="padding: 10px; text-align: right; border-bottom: 2px solid #d1d5db;">Cost</th>
              <th style="padding: 10px; text-align: left; border-bottom: 2px solid #d1d5db;">Requested By</th>
              <th style="padding: 10px; text-align: left; border-bottom: 2px solid #d1d5db;">Money Received By</th>
              <th style="padding: 10px; text-align: left; border-bottom: 2px solid #d1d5db;">Approved By</th>
              <th style="padding: 10px; text-align: center; border-bottom: 2px solid #d1d5db;">Status</th>
            </tr>
          </thead>
          <tbody>
            ${filteredRequisitions.value.map(req => `
              <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 8px; white-space: nowrap;">${formatDate(req.date_requested)}</td>
                <td style="padding: 8px;">${req.item_name || req.item?.name || 'Unknown'}</td>
                <td style="padding: 8px; text-align: right;">${req.quantity_requested} ${getItemUnit(req)}</td>
                <td style="padding: 8px; text-align: right; font-weight: bold; color: #059669;">${req.estimated_cost ? formatCurrency(req.estimated_cost) : '-'}</td>
                <td style="padding: 8px;">${req.requested_by}</td>
                <td style="padding: 8px;">${req.money_received_by || '-'}</td>
                <td style="padding: 8px;">${req.approved_by || '-'}</td>
                <td style="padding: 8px; text-align: center;">
                  <span style="padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; background-color: ${getStatusColor(req.status)}20; color: ${getStatusColor(req.status)};">
                    ${getStatusLabel(req.status)}
                  </span>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
        ` : `
        <p style="text-align: center; padding: 20px; color: #6b7280;">No purchase requests found for the selected criteria.</p>
        `}
      </div>
      
      <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e5e7eb; color: #6b7280; font-size: 12px; text-align: center;">
        <p>This report was generated by BITZ Kitchen System</p>
        <p>© ${new Date().getFullYear()} BITZ - Kitchen Inventory Management</p>
      </div>
    </div>
  `
  
  printReportContent(reportHtml)
}

const printReportContent = (html) => {
  const printWindow = window.open('', '_blank')
  
  if (!printWindow) {
    toast.error('Pop-up blocked. Please allow pop-ups for this site.')
    return
  }
  
  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>BITZ Kitchen Report</title>
        <meta charset="UTF-8">
        <style>
          body { 
            margin: 0; 
            padding: 0; 
            font-family: 'Roboto', Arial, sans-serif;
          }
          @media print {
            @page { margin: 1cm; }
          }
        </style>
      </head>
      <body>
        ${html}
      </body>
    </html>
  `)
  printWindow.document.close()
  
  // Wait for images and content to load before printing
  setTimeout(() => {
    printWindow.focus()
    printWindow.print()
    toast.success('Report generated and opened for printing')
  }, 500)
}

const printReport = () => {
  reportPeriod.value = 'all'
  generateCustomReport()
}

onMounted(() => {
  loadAnalytics()
})
</script>

<script>
export default {
  name: 'AnalyticsView'
}
</script>

