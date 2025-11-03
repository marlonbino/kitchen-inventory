<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-3 sm:p-4 md:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Page Header -->
      <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Purchase Requests</h1>
          <p class="text-gray-600 dark:text-gray-200 font-medium mt-1">Request purchases & approve orders</p>
        </div>
        <div class="flex gap-2">
          <BaseButton
            v-if="selectedRequisitions.length > 0 && activeTab === 'pending' && isAdmin"
            variant="primary"
            @click="showBulkApproveConfirm = true"
            :disabled="bulkActionLoading"
          >
            <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Approve All ({{ selectedRequisitions.length }})
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
            New Purchase Request
          </BaseButton>
        </div>
      </div>

      <!-- Admin Approve All Banner -->
      <div
        v-if="selectedRequisitions.length > 0 && activeTab === 'pending' && isAdmin"
        class="mb-6 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-2 border-green-300 dark:border-green-700 rounded-xl p-6 shadow-elegant"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-green-500 rounded-full">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-green-900 dark:text-green-100">
                Approving {{ selectedRequisitions.length }} Request(s)
              </h3>
              <p class="text-sm text-green-700 dark:text-green-300 mt-1">
                Total amount needed for approval
              </p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-3xl font-extrabold text-green-900 dark:text-green-100">
              {{ formatCurrency(totalApprovalCost) }}
            </p>
            <p class="text-xs text-green-700 dark:text-green-300 mt-1">
              Kenyan Shillings
            </p>
          </div>
        </div>
      </div>

      <!-- Statistics Cards with Circular Badges -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6">
        <!-- Total Pending -->
        <div class="group flex flex-col items-center w-full bg-gradient-to-br from-yellow-900/30 to-neutral-900 dark:from-yellow-900/30 dark:to-neutral-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-yellow-500/30">
          <div class="circular-badge circular-badge-yellow cursor-pointer group-hover:scale-110 transition-transform duration-300">
            <div class="circular-badge-number">
              {{ pendingCount }}
            </div>
          </div>
          <div class="mt-6 text-center w-full">
            <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Pending Approval</h3>
            <p class="text-xs text-gray-500 mt-2">Awaiting admin</p>
          </div>
        </div>

        <!-- Most Requested Item -->
        <div class="group flex flex-col items-center w-full bg-gradient-to-br from-blue-900/30 to-neutral-900 dark:from-blue-900/30 dark:to-neutral-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-blue-500/30">
          <div class="circular-badge circular-badge-blue cursor-pointer group-hover:scale-110 transition-transform duration-300">
            <div class="circular-badge-number">
              {{ mostRequestedItem?.count || 0 }}
            </div>
          </div>
          <div class="mt-6 text-center w-full">
            <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Most Requested</h3>
            <p class="text-sm font-bold text-blue-300 truncate w-full">
              {{ mostRequestedItem?.name || 'N/A' }}
            </p>
            <p class="text-xs text-gray-500 mt-2">Top requested</p>
          </div>
        </div>

        <!-- Urgent (0 Stock) -->
        <div class="group flex flex-col items-center w-full bg-gradient-to-br from-red-900/30 to-neutral-900 dark:from-red-900/30 dark:to-neutral-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-red-500/30">
          <div class="circular-badge circular-badge-red cursor-pointer group-hover:scale-110 transition-transform duration-300">
            <div class="circular-badge-number">
              {{ urgentCount }}
            </div>
          </div>
          <div class="mt-6 text-center w-full">
            <div class="flex items-center justify-center gap-2 flex-wrap mb-2">
              <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider">Urgent</h3>
              <span
                v-if="urgentCount > 0"
                class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold bg-red-500 text-white animate-pulse"
              >
                ALERT
              </span>
            </div>
            <p class="text-xs text-gray-500 mt-2">0 stock items</p>
          </div>
        </div>
      </div>

      <!-- Tabs and Search -->
      <div class="mb-6 bg-white dark:bg-neutral-800 rounded-xl shadow-elegant p-6 border border-gray-100 dark:border-neutral-700">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Tabs -->
          <div class="flex border-b border-gray-200 dark:border-neutral-700">
            <button
              v-for="tab in tabs"
              :key="tab.value"
              @click="activeTab = tab.value"
              class="px-4 py-2 text-sm font-medium border-b-2 transition-colors cursor-pointer touch-manipulation"
              :class="activeTab === tab.value
                ? 'border-blue-500 dark:border-blue-400 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-white hover:border-gray-300 dark:hover:border-neutral-600'"
            >
              {{ tab.label }}
              <span v-if="tab.count !== undefined" class="ml-2 px-2 py-0.5 text-xs rounded-full"
                :class="activeTab === tab.value ? 'bg-blue-100 dark:bg-blue-400 text-blue-800 dark:text-black' : 'bg-gray-100 dark:bg-neutral-700 text-gray-600 dark:text-gray-300'">
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
        </div>
      </div>

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
          <p class="mt-2 text-gray-500">No purchase requests found</p>
          <BaseButton variant="primary" @click="openCreateModal" class="mt-4">
            Create First Request
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Requisitions Table -->
      <div v-else class="hidden md:block">
<div class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
          <div class="overflow-x-auto custom-scrollbar">
            <table class="min-w-full">
              <thead class="bg-neutral-800/50 dark:bg-neutral-800/50">
                <tr>
                  <th v-if="activeTab === 'pending' && isAdmin" class="px-6 py-4 text-left">
                    <input
                      type="checkbox"
                      :checked="allSelected"
                      @change="toggleSelectAll"
                      class="rounded border-neutral-600 bg-neutral-800 text-blue-500 focus:ring-blue-500 focus:ring-offset-neutral-800 w-4 h-4"
                    />
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider cursor-pointer hover:bg-neutral-700 dark:hover:bg-neutral-700 transition-colors"
                    @click="sortBy('date_requested')"
                  >
                    <div class="flex items-center gap-2">
                      DATE
                      <svg v-if="sortField === 'date_requested'" class="w-4 h-4 text-blue-500 dark:text-blue-400" :class="sortDirection === 'asc' ? '' : 'transform rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                      </svg>
                    </div>
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    ITEM
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    QTY
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    COST (KES)
                  </th>
                  <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                    REQUESTED BY
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
                  v-for="req in sortedRequisitions"
                  :key="req.id"
                  class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-all duration-200"
                >
                  <td v-if="activeTab === 'pending' && isAdmin" class="px-6 py-5 whitespace-nowrap">
                    <input
                      type="checkbox"
                      :checked="selectedRequisitions.includes(req.id)"
                      @change="toggleSelection(req.id)"
                      class="rounded border-neutral-600 bg-neutral-800 text-blue-500 focus:ring-blue-500 focus:ring-offset-neutral-800 w-4 h-4"
                    />
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <span class="text-sm text-gray-300 dark:text-gray-300">{{ formatDate(req.date_requested) }}</span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap">
                    <div class="flex items-center gap-2">
                      <div class="text-sm font-semibold text-white dark:text-white">
                        {{ req.item_name || req.item?.name || 'Unknown' }}
                      </div>
                      <span v-if="isUrgent(req)" class="px-2 py-0.5 text-xs font-bold bg-red-400 dark:bg-red-400 text-black dark:text-black rounded-full">
                        URGENT
                      </span>
                    </div>
                    <div class="mt-1">
                      <StockBadge
                        :current="getItemStock(req)"
                        :minimum="getItemMinStock(req)"
                        :show-percentage="false"
                      />
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
                    <span
                      class="inline-flex items-center px-3 py-1.5 text-xs font-bold rounded-full"
                      :class="getStatusBadgeClassDark(req.status)"
                    >
                      {{ getStatusLabel(req.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-5 whitespace-nowrap text-right">
                    <div class="flex items-center justify-end gap-2">
                      <template v-if="req.status === 'pending' && isAdmin">
                        <button
                          @click="confirmApprove(req)"
                          :disabled="actionLoading"
                          class="text-green-500 dark:text-green-400 hover:text-green-400 dark:hover:text-green-300 rounded-lg p-2 transition-colors duration-200"
                          title="Approve"
                        >
                          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                          </svg>
                        </button>
                        <button
                          @click="confirmReject(req)"
                          :disabled="actionLoading"
                          class="text-red-500 dark:text-red-400 hover:text-red-400 dark:hover:text-red-300 rounded-lg p-2 transition-colors duration-200"
                          title="Reject"
                        >
                          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </template>
                      <template v-else-if="req.status === 'awaiting_delivery' && isAdmin && !req.assigned_to">
                        <button
                          @click="openAssignModal(req)"
                          :disabled="actionLoading"
                          class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 rounded-lg p-2 transition-colors duration-200"
                          title="Assign Delivery"
                        >
                          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                          </svg>
                        </button>
                      </template>
                      <template v-else-if="req.status === 'awaiting_delivery' && canConfirmReceipt(req)">
                        <button
                          @click="confirmReceived(req)"
                          :disabled="actionLoading"
                          class="text-green-500 dark:text-green-400 hover:text-green-400 dark:hover:text-green-300 rounded-lg p-2 transition-colors duration-200"
                          title="Confirm Received"
                        >
                          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                          </svg>
                        </button>
                      </template>
                      <button
                        v-else
                        @click="viewDetails(req)"
                        class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 rounded-lg p-2 transition-colors duration-200"
                        title="View Details"
                      >
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
        </div>
      </div>

      <!-- Mobile Card View -->
      <div v-if="!loading && !error && filteredRequisitions.length > 0" class="md:hidden space-y-4">
        <div
          v-for="req in sortedRequisitions"
          :key="req.id"
          class="bg-neutral-800 dark:bg-neutral-800 rounded-xl shadow-elegant border border-neutral-700 dark:border-neutral-700 p-4"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-white dark:text-white">{{ req.item_name || req.item?.name || 'Unknown' }}</h3>
              <p class="text-sm text-gray-300 dark:text-gray-300 mt-1">{{ req.requested_by }}</p>
            </div>
            <span
              class="inline-flex items-center px-3 py-1.5 text-xs font-bold rounded-full"
              :class="getStatusBadgeClassDark(req.status)"
            >
              {{ getStatusLabel(req.status) }}
            </span>
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

          <div v-if="req.status === 'pending' && isAdmin" class="flex gap-2 pt-3 border-t dark:border-neutral-700">
            <button
              @click="confirmApprove(req)"
              :disabled="actionLoading"
              class="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 text-sm"
            >
              Approve
            </button>
            <button
              @click="confirmReject(req)"
              :disabled="actionLoading"
              class="flex-1 bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 text-sm"
            >
              Reject
            </button>
          </div>
          <div v-else-if="req.status === 'awaiting_delivery' && isAdmin && !req.assigned_to" class="pt-3 border-t dark:border-neutral-700">
            <button
              @click="openAssignModal(req)"
              :disabled="actionLoading"
              class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 text-sm"
            >
              Assign Delivery
            </button>
          </div>
          <div v-else-if="req.status === 'awaiting_delivery' && canConfirmReceipt(req)" class="pt-3 border-t dark:border-neutral-700">
            <button
              @click="confirmReceived(req)"
              :disabled="actionLoading"
              class="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 text-sm"
            >
              Confirm Received
            </button>
          </div>
          <div v-else class="pt-3 border-t dark:border-neutral-700">
            <button
              @click="viewDetails(req)"
              class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 text-sm"
            >
              View Details
            </button>
          </div>
        </div>
      </div>

      <!-- Create Requisition Modal -->
      <BaseModal :show="showCreateModal" title="New Purchase Request" @close="closeCreateModal">
        <RequisitionForm
          :loading="createLoading"
          @submit="handleCreateRequisition"
          @cancel="closeCreateModal"
        />
      </BaseModal>

      <!-- View Details Modal -->
      <BaseModal :show="showDetailsModal" title="Purchase Request Details" @close="closeDetailsModal">
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
        title="Approve Purchase Request"
        :message="`Approve purchase request for ${approveRequisition?.quantity_requested} ${getItemUnit(approveRequisition)} of ${approveRequisition?.item_name || 'item'}?`"
        confirm-text="Approve"
        cancel-text="Cancel"
        variant="primary"
        @confirm="handleApprove"
        @cancel="cancelApprove"
      />

      <!-- Rejection Confirmation -->
      <ConfirmDialog
        :show="showRejectConfirm"
        title="Reject Purchase Request"
        :message="`Reject purchase request for ${rejectRequisition?.quantity_requested} ${getItemUnit(rejectRequisition)} of ${rejectRequisition?.item_name || 'item'}?`"
        confirm-text="Reject"
        cancel-text="Cancel"
        variant="danger"
        @confirm="handleReject"
        @cancel="cancelReject"
      />

      <!-- Bulk Approve Confirmation -->
      <ConfirmDialog
        :show="showBulkApproveConfirm"
        title="Approve All Purchase Requests"
        :message="`Approve ${selectedRequisitions.length} purchase request(s)?`"
        confirm-text="Approve All"
        cancel-text="Cancel"
        variant="primary"
        @confirm="handleBulkApprove"
        @cancel="showBulkApproveConfirm = false"
      />

      <!-- Assign Delivery Modal -->
      <BaseModal :show="showAssignModal" title="Assign Delivery Person" @close="closeAssignModal">
        <div v-if="assignRequisition" class="space-y-4">
          <div class="p-3 bg-blue-50 border border-blue-200 rounded-md">
            <p class="text-sm font-medium text-blue-900">Assign who will receive this delivery</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Person to Receive</label>
            <input
              v-model="assignToName"
              type="text"
              placeholder="Enter recipient name..."
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span class="text-gray-500">Item:</span>
              <span class="ml-2 font-medium">{{ assignRequisition.item_name || 'Unknown' }}</span>
            </div>
            <div>
              <span class="text-gray-500">Quantity:</span>
              <span class="ml-2 font-medium">{{ assignRequisition.quantity_requested }} {{ getItemUnit(assignRequisition) }}</span>
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-4 border-t">
            <BaseButton variant="secondary" @click="closeAssignModal" :disabled="actionLoading">
              Cancel
            </BaseButton>
            <BaseButton variant="primary" @click="handleAssignDelivery" :disabled="actionLoading || !assignToName.trim()">
              Assign
            </BaseButton>
          </div>
        </div>
      </BaseModal>

      <!-- Receive Confirmation Modal -->
      <BaseModal :show="showReceiveConfirm" title="Confirm Receipt" @close="showReceiveConfirm = false">
        <div v-if="selectedRequisition" class="space-y-4">
          <div class="p-3 bg-blue-50 border border-blue-200 rounded-md">
            <p class="text-sm font-medium text-blue-900">Please confirm the quantity you received</p>
          </div>
          
          <div class="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span class="text-gray-500">Item:</span>
              <span class="ml-2 font-medium">{{ selectedRequisition.item_name || 'Unknown' }}</span>
            </div>
            <div>
              <span class="text-gray-500">Expected:</span>
              <span class="ml-2 font-medium">{{ selectedRequisition.quantity_requested }} {{ getItemUnit(selectedRequisition) }}</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Quantity Received *
            </label>
            <input
              v-model.number="quantityReceived"
              type="number"
              :min="1"
              :max="selectedRequisition.quantity_requested"
              :placeholder="selectedRequisition.quantity_requested"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p class="mt-1 text-xs text-gray-500">
              Maximum: {{ selectedRequisition.quantity_requested }} {{ getItemUnit(selectedRequisition) }}
            </p>
          </div>

          <div v-if="quantityReceived < selectedRequisition.quantity_requested">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Reason for Shortfall *
            </label>
            <textarea
              v-model="receiptNotes"
              rows="3"
              placeholder="Explain why you received less than requested..."
              class="block w-full px-3 py-2 border border-red-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
            />
            <p class="mt-1 text-xs text-red-500">
              Required when quantity received is less than requested
            </p>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t">
            <BaseButton variant="secondary" @click="showReceiveConfirm = false" :disabled="actionLoading">
              Cancel
            </BaseButton>
            <BaseButton 
              variant="primary" 
              @click="handleConfirmReceived" 
              :disabled="actionLoading || quantityReceived <= 0 || quantityReceived > selectedRequisition.quantity_requested || (quantityReceived < selectedRequisition.quantity_requested && !receiptNotes)"
            >
              Confirm Received
            </BaseButton>
          </div>
        </div>
      </BaseModal>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import { useDebounce } from '../composables/useDebounce'
import { getUserInfo } from '../services/api.js'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import StockBadge from '../components/StockBadge.vue'
import RequisitionForm from '../components/RequisitionForm.vue'

const store = useInventoryStore()
const toast = useToast()

// Current user info
const currentUser = ref(null)
const isAdmin = computed(() => currentUser.value?.role === 'admin')

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
const showAssignModal = ref(false)
const showReceiveConfirm = ref(false)
const selectedRequisition = ref(null)
const approveRequisition = ref(null)
const rejectRequisition = ref(null)
const assignRequisition = ref(null)
const assignToName = ref('')
const quantityReceived = ref(null)
const receiptNotes = ref('')

// Tabs configuration
const tabs = computed(() => {
  const all = requisitions.value.length
  const pending = requisitions.value.filter(r => r.status === 'pending').length
  const awaiting = requisitions.value.filter(r => r.status === 'awaiting_delivery').length
  const rejected = requisitions.value.filter(r => r.status === 'rejected').length

  return [
    { value: 'all', label: 'All', count: all },
    { value: 'pending', label: 'Pending Approval', count: pending },
    { value: 'awaiting_delivery', label: 'Awaiting Delivery', count: awaiting },
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

// Calculate total cost of selected requisitions
const totalApprovalCost = computed(() => {
  let total = 0
  selectedRequisitions.value.forEach(reqId => {
    const req = requisitions.value.find(r => r.id === reqId)
    if (req) {
      const item = store.itemById(req.item_id || req.item?.id)
      if (item && item.price_per_unit) {
        total += parseFloat(item.price_per_unit) * req.quantity_requested
      }
    }
  })
  return total
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
    awaiting_delivery: 'Awaiting Delivery',
    delivered: 'Delivered',
    rejected: 'Rejected'
  }
  return labels[status] || status
}

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    approved: 'bg-blue-100 text-blue-800',
    awaiting_delivery: 'bg-orange-100 text-orange-800',
    delivered: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusBadgeClassDark = (status) => {
  const classes = {
    pending: 'bg-yellow-400 dark:bg-yellow-400 text-black dark:text-black',
    approved: 'bg-blue-400 dark:bg-blue-400 text-black dark:text-black',
    awaiting_delivery: 'bg-orange-400 dark:bg-orange-400 text-black dark:text-black',
    delivered: 'bg-green-400 dark:bg-green-400 text-black dark:text-black',
    rejected: 'bg-red-400 dark:bg-red-400 text-black dark:text-black'
  }
  return classes[status] || 'bg-gray-400 dark:bg-gray-400 text-black dark:text-black'
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

const getReqCost = (req) => {
  if (!req) return '—'
  const item = store.itemById(req.item_id || req.item?.id)
  if (!item || !item.price_per_unit) return '—'
  const cost = parseFloat(item.price_per_unit) * req.quantity_requested
  return formatCurrency(cost)
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

const canConfirmReceipt = (req) => {
  if (!req) return false
  if (!isAdmin.value && !req.assigned_to) return false
  if (!isAdmin.value && req.assigned_to && req.assigned_to.toLowerCase() !== currentUser.value?.username.toLowerCase()) {
    return false
  }
  return true
}

const openAssignModal = (req) => {
  assignRequisition.value = req
  showAssignModal.value = true
}

const closeAssignModal = () => {
  showAssignModal.value = false
  assignRequisition.value = null
  assignToName.value = ''
}

const handleAssignDelivery = async () => {
  if (!assignRequisition.value || !assignToName.value.trim()) return

  actionLoading.value = true
  try {
    await store.assignDelivery(assignRequisition.value.id, assignToName.value.trim())
    toast.success('Delivery assigned successfully')
    closeAssignModal()
    await loadRequisitions()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to assign delivery'
    toast.error(errorMessage)
  } finally {
    actionLoading.value = false
  }
}

const confirmReceived = (req) => {
  if (!req) return
  
  selectedRequisition.value = req
  quantityReceived.value = req.quantity_requested
  receiptNotes.value = ''
  showReceiveConfirm.value = true
}

const handleConfirmReceived = async () => {
  if (!selectedRequisition.value) return

  actionLoading.value = true
  try {
    await store.confirmReceived(
      selectedRequisition.value.id,
      quantityReceived.value,
      receiptNotes.value
    )
    toast.success('Receipt confirmed successfully! Stock has been added.')
    showReceiveConfirm.value = false
    quantityReceived.value = null
    receiptNotes.value = ''
    await loadRequisitions()
    await store.fetchItems()
  } catch (err) {
    const errorMessage = err.response?.data?.error || err.message || 'Failed to confirm receipt'
    toast.error(errorMessage)
  } finally {
    actionLoading.value = false
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

const formatCurrency = (value) => {
  if (!value) return 'KSh 0.00'
  // Format number with commas and add KSh prefix
  return 'KSh ' + new Intl.NumberFormat('en-KE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

// Watch tab changes to clear selections
watch(() => activeTab.value, () => {
  selectedRequisitions.value = []
})

// Lifecycle
onMounted(async () => {
  // Load user info
  try {
    const user = await getUserInfo()
    currentUser.value = user
  } catch (err) {
    console.error('Failed to get user info:', err)
  }
  
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

