<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-3 sm:p-4 md:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Page Header -->
      <div class="mb-8 fade-up-enter-active">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-2 bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">Kitchen Overview</h1>
        <p class="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-300 font-medium">Quick view of kitchen status</p>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="loading && !dashboardStats" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="n in 4" :key="n" class="bg-white dark:bg-neutral-800 rounded-lg shadow-md p-6 animate-pulse">
            <div class="h-4 bg-gray-200 dark:bg-neutral-700 rounded w-1/2 mb-3"></div>
            <div class="h-8 bg-gray-200 dark:bg-neutral-700 rounded w-3/4"></div>
          </div>
        </div>
        <div class="bg-white dark:bg-neutral-800 rounded-lg shadow-md p-6 animate-pulse">
          <div class="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div class="space-y-3">
            <div v-for="n in 5" :key="n" class="h-16 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error && !loading" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-600 dark:text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <p class="text-red-800 dark:text-red-400">Error loading dashboard: {{ error }}</p>
        </div>
        <button
          @click="loadDashboard"
          class="mt-3 text-sm text-red-700 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 underline"
        >
          Try again
        </button>
      </div>

      <!-- Dashboard Content -->
      <div v-else class="space-y-6">
        <!-- Statistics Cards with Circular Badges -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          <!-- Total Items Card -->
          <div class="group flex flex-col items-center w-full bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-neutral-700">
            <div class="circular-badge circular-badge-blue cursor-pointer group-hover:scale-110 transition-transform duration-300">
              <div class="circular-badge-number">
                {{ dashboardStats?.total_items || 0 }}
              </div>
            </div>
            <div class="mt-6 text-center w-full">
              <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Total Items</h3>
              <p class="text-xs text-gray-500 mt-2">Current inventory</p>
            </div>
          </div>

          <!-- Low Stock Items Card -->
          <div class="group flex flex-col items-center w-full bg-gradient-to-br from-red-900/30 to-neutral-900 dark:from-red-900/30 dark:to-neutral-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-red-500/30 cursor-pointer" @click="navigateToLowStock">
            <div class="circular-badge circular-badge-red group-hover:scale-110 transition-transform duration-300">
              <div class="circular-badge-number">
                {{ dashboardStats?.low_stock_count || 0 }}
              </div>
            </div>
            <div class="mt-6 text-center w-full">
              <div class="flex items-center justify-center gap-2 flex-wrap mb-2">
                <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider">Running Low</h3>
                <span
                  v-if="(dashboardStats?.low_stock_count || 0) > 0"
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold bg-red-500 text-white animate-pulse"
                >
                  URGENT
                </span>
              </div>
              <p class="text-xs text-gray-500 mt-2">Items running low</p>
            </div>
          </div>

          <!-- In Transit Card -->
          <div class="group flex flex-col items-center w-full bg-gradient-to-br from-yellow-900/30 to-neutral-900 dark:from-yellow-900/30 dark:to-neutral-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-yellow-500/30 cursor-pointer" @click="navigateToRequisitions">
            <div class="circular-badge circular-badge-yellow group-hover:scale-110 transition-transform duration-300">
              <div class="circular-badge-number">
                {{ dashboardStats?.awaiting_delivery_count || 0 }}
              </div>
            </div>
            <div class="mt-6 text-center w-full">
              <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">In Transit</h3>
              <p class="text-xs text-gray-500 mt-2">Pending orders</p>
            </div>
          </div>

          <!-- Today's Movements Card -->
          <div class="group flex flex-col items-center w-full bg-gradient-to-br from-green-900/30 to-neutral-900 dark:from-green-900/30 dark:to-neutral-900 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-green-500/30">
            <div class="circular-badge circular-badge-green group-hover:scale-110 transition-transform duration-300">
              <div class="circular-badge-number">
                {{ todayMovementsCount }}
              </div>
            </div>
            <div class="mt-6 text-center w-full">
              <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Today's Activity</h3>
              <p class="text-xs text-gray-500 mt-2">Movements today</p>
            </div>
          </div>
        </div>

        <!-- Low Stock Alert Section -->
        <div>
          <div class="mb-4">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-1">Restock Now!</h2>
            <p class="text-sm text-gray-600 dark:text-gray-300">Items below minimum level</p>
          </div>
          
          <div v-if="lowStockItemsLoading" class="bg-neutral-800 dark:bg-neutral-800 rounded-xl shadow-elegant overflow-hidden border border-neutral-700 dark:border-neutral-700">
            <div class="p-6 space-y-3">
              <div v-for="n in 5" :key="n" class="h-16 bg-neutral-700 dark:bg-neutral-700 rounded animate-pulse"></div>
            </div>
          </div>
          
          <div v-else-if="lowStockItems.length === 0" class="bg-neutral-800 dark:bg-neutral-800 rounded-xl shadow-elegant border border-neutral-700 dark:border-neutral-700">
            <div class="text-center py-12">
              <div class="inline-flex p-4 bg-green-400 dark:bg-green-400 rounded-full mb-4">
                <svg class="h-12 w-12 text-black dark:text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="text-lg font-semibold text-white dark:text-white">All stocked up!</p>
              <p class="mt-1 text-gray-300 dark:text-gray-300">No low stock items at the moment</p>
            </div>
          </div>
          
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
                        UNIT
                      </th>
                      <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                        STOCK AVAILABLE
                      </th>
                      <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                        MINIMUM LEVEL
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
                      v-for="item in displayedLowStockItems"
                      :key="item.id"
                      class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-all duration-200 cursor-pointer"
                      @click="navigateToLowStock"
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
                        <span class="inline-flex items-center px-3 py-1.5 text-xs font-bold bg-red-400 dark:bg-red-400 text-black dark:text-black rounded-full">
                          <span class="w-2 h-2 bg-black dark:bg-black rounded-full mr-2"></span>
                          Restock Needed
                        </span>
                      </td>
                      <td class="px-6 py-5 whitespace-nowrap text-right">
                        <div class="flex items-center justify-end gap-2">
                          <router-link
                            to="/low-stock"
                            class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 rounded-lg p-2 transition-colors duration-200"
                            title="View All"
                            @click.stop
                          >
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                            </svg>
                          </router-link>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <!-- Show More / Show Less Button -->
            <div v-if="lowStockItems.length > 0" class="px-6 py-4 border-t border-transparent dark:border-transparent bg-transparent dark:bg-transparent">
              <div class="flex items-center justify-center gap-3">
                <button
                  v-if="hasMoreLowStockItems"
                  @click="showMoreLowStock"
                  class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
                >
                  See More ({{ lowStockItems.length - lowStockItemsToShow }} remaining)
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <button
                  v-if="showLessLowStockButton"
                  @click="showLessLowStock"
                  class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
                >
                  Show Less
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
                <router-link
                  v-if="!hasMoreLowStockItems && !showLessLowStockButton"
                  to="/low-stock"
                  class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm"
                >
                  View all low stock items →
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- Mobile View -->
          <div v-if="!lowStockItemsLoading && lowStockItems.length > 0" class="md:hidden space-y-3">
            <div
              v-for="item in displayedLowStockItems"
              :key="item.id"
              class="bg-neutral-800 dark:bg-neutral-800 rounded-lg p-4 border border-neutral-700 dark:border-neutral-700"
            >
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-semibold text-white dark:text-white">{{ item.name }}</h4>
                <StockBadge
                  :current="item.current_stock"
                  :minimum="item.min_stock_level"
                  :show-percentage="false"
                />
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-300 dark:text-gray-300">
                <span class="px-2 py-1 text-xs font-medium bg-neutral-700 dark:bg-neutral-700 text-gray-300 dark:text-gray-300 rounded-full">
                  {{ item.category_name }}
                </span>
                <span>{{ item.unit }}</span>
              </div>
            </div>
            <!-- Show More / Show Less Button (Mobile) -->
            <div v-if="lowStockItems.length > 0" class="flex items-center justify-center gap-3 pt-2">
              <button
                v-if="hasMoreLowStockItems"
                @click="showMoreLowStock"
                class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
              >
                See More ({{ lowStockItems.length - lowStockItemsToShow }} remaining)
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <button
                v-if="showLessLowStockButton"
                @click="showLessLowStock"
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

        <!-- Pending Deliveries Section -->
        <div v-if="pendingDeliveries.length > 0">
          <div class="mb-4">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-1">Confirm Deliveries</h2>
            <p class="text-sm text-gray-600 dark:text-gray-300">Approve your ordered items</p>
          </div>
          
          <div class="bg-neutral-800 dark:bg-neutral-800 rounded-xl shadow-elegant overflow-hidden border border-neutral-700 dark:border-neutral-700">
            <div class="overflow-x-auto custom-scrollbar">
              <table class="min-w-full divide-y divide-neutral-700 dark:divide-neutral-700">
                <thead class="bg-neutral-800 dark:bg-neutral-800 border-b-2 border-neutral-700 dark:border-neutral-700">
                  <tr>
                    <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                      ITEM
                    </th>
                    <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                      QUANTITY
                    </th>
                    <th class="px-6 py-4 text-left text-xs font-bold text-white uppercase tracking-wider">
                      ORDERED BY
                    </th>
                    <th class="px-6 py-4 text-right text-xs font-bold text-white uppercase tracking-wider">
                      ACTION
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-neutral-800 dark:bg-neutral-800 divide-y divide-neutral-700 dark:divide-neutral-700">
                  <tr
                    v-for="req in pendingDeliveries"
                    :key="req.id"
                    class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-colors duration-150"
                  >
                    <td class="px-6 py-5 whitespace-nowrap">
                      <div class="text-sm font-semibold text-white dark:text-white">
                        {{ req.item_name || req.item?.name || 'Unknown' }}
                      </div>
                    </td>
                    <td class="px-6 py-5 whitespace-nowrap">
                      <span class="text-sm text-gray-300 dark:text-gray-300 font-medium">
                        {{ req.quantity_requested }} {{ getItemUnitForReq(req) }}
                      </span>
                    </td>
                    <td class="px-6 py-5 whitespace-nowrap">
                      <span class="text-sm text-gray-300 dark:text-gray-300">{{ req.requested_by }}</span>
                    </td>
                    <td class="px-6 py-5 whitespace-nowrap text-right">
                      <button
                        @click="handleQuickConfirmDelivery(req)"
                        class="inline-flex items-center px-4 py-2 bg-green-500 hover:bg-green-600 text-white text-sm font-semibold rounded-lg transition-colors duration-200"
                      >
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        Confirm
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Recent Stock Movements Section -->
        <div>
          <div class="mb-4">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-1">Recent Stock Movements</h2>
            <p class="text-sm text-gray-600 dark:text-gray-300">Last 10 stock movements</p>
          </div>
          
          <div v-if="movementsLoading" class="bg-neutral-800 dark:bg-neutral-800 rounded-xl shadow-elegant overflow-hidden border border-neutral-700 dark:border-neutral-700">
            <div class="p-6 space-y-3">
              <div v-for="n in 10" :key="n" class="h-16 bg-neutral-700 dark:bg-neutral-700 rounded animate-pulse"></div>
            </div>
          </div>
          
          <div v-else-if="recentMovements.length === 0" class="bg-neutral-800 dark:bg-neutral-800 rounded-xl shadow-elegant border border-neutral-700 dark:border-neutral-700">
            <div class="text-center py-12">
              <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
              <p class="mt-2 text-gray-500 dark:text-gray-400">No stock movements yet</p>
            </div>
          </div>
          
          <div v-else class="hidden md:block">
            <div class="bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden">
              <div class="overflow-x-auto custom-scrollbar">
                <table class="min-w-full">
                  <thead class="bg-neutral-800/50 dark:bg-neutral-800/50">
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
                      <th class="px-6 py-4 text-right text-xs font-bold text-white uppercase tracking-wider">
                        ACTIONS
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="movement in displayedMovements"
                      :key="movement.id"
                      class="hover:bg-neutral-700/50 dark:hover:bg-neutral-700/50 transition-all duration-200"
                    >
                      <td class="px-6 py-5 whitespace-nowrap">
                        <span class="text-sm text-gray-300 dark:text-gray-300">{{ formatRelativeTime(movement.date) }}</span>
                      </td>
                      <td class="px-6 py-5 whitespace-nowrap">
                        <div class="text-sm font-semibold text-white dark:text-white">
                          {{ movement.item_name || movement.item?.name || 'Unknown' }}
                        </div>
                        <div class="mt-1">
                          <span class="px-2 py-1 text-xs font-medium bg-neutral-700 dark:bg-neutral-700 text-gray-300 dark:text-gray-300 rounded-full">
                            {{ getItemCategory(movement) }}
                          </span>
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
                      <td class="px-6 py-5 whitespace-nowrap text-right">
                        <span class="text-sm text-gray-400 dark:text-gray-500">—</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!-- Show More / Show Less Button -->
              <div v-if="recentMovements.length > 0" class="px-6 py-4 border-t border-transparent dark:border-transparent bg-transparent dark:bg-transparent">
                <div class="flex items-center justify-between gap-3">
                  <router-link
                    to="/movements"
                    class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
                  >
                    View All Movements
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </router-link>
                  <div class="flex items-center gap-3">
                    <button
                      v-if="hasMoreMovements"
                      @click="showMoreMovements"
                      class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
                    >
                      See More ({{ recentMovements.length - movementsToShow }} remaining)
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                      </svg>
                    </button>
                    <button
                      v-if="showLessMovementsButton"
                      @click="showLessMovements"
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
          </div>
          
          <!-- Mobile View -->
          <div v-if="!movementsLoading && recentMovements.length > 0" class="md:hidden space-y-2">
            <div
              v-for="movement in displayedMovements"
              :key="movement.id"
              class="bg-neutral-800 dark:bg-neutral-800 rounded-lg p-4 border border-neutral-700 dark:border-neutral-700"
            >
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-semibold text-white dark:text-white">
                  {{ movement.item_name || movement.item?.name || 'Unknown Item' }}
                </h4>
                <span
                  class="inline-flex items-center px-2 py-1 text-xs font-bold rounded-full"
                  :class="getMovementTypeBadgeClassDark(movement.movement_type)"
                >
                  {{ getMovementTypeLabel(movement.movement_type) }}
                </span>
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-300 dark:text-gray-300">
                <span>{{ getQuantityPrefix(movement.movement_type) }}{{ movement.quantity }} {{ getItemUnit(movement) }}</span>
                <span>•</span>
                <span>{{ formatRelativeTime(movement.date) }}</span>
              </div>
            </div>
            <!-- Show More / Show Less Button (Mobile) -->
            <div v-if="recentMovements.length > 0" class="flex items-center justify-center gap-3 pt-2">
              <button
                v-if="hasMoreMovements"
                @click="showMoreMovements"
                class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
              >
                See More ({{ recentMovements.length - movementsToShow }} remaining)
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <button
                v-if="showLessMovementsButton"
                @click="showLessMovements"
                class="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 font-semibold text-sm flex items-center gap-2 transition-colors duration-200"
              >
                Show Less
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                </svg>
              </button>
              <router-link
                v-if="!hasMoreMovements && !showLessMovementsButton && recentMovements.length >= 10"
                to="/movements"
                class="text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 font-semibold text-sm"
              >
                View all movements →
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from 'vue-toastification'
import { getUserInfo } from '../services/api.js'
import BaseCard from '../components/BaseCard.vue'
import StockBadge from '../components/StockBadge.vue'

const router = useRouter()
const store = useInventoryStore()
const toast = useToast()

// Current user info
const currentUser = ref(null)

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
  let movements = []
  if (store.stockMovements.length > 0) {
    movements = store.stockMovements.slice(0, 10)
  } else if (dashboardStats.value?.recent_movements) {
    movements = dashboardStats.value.recent_movements.slice(0, 10)
  }
  
  // Filter out incomplete or invalid movements (must have item name and quantity)
  return movements.filter(movement => 
    movement &&
    movement.id !== null &&
    movement.id !== undefined &&
    (movement.item_name || movement.item?.name) &&
    movement.quantity !== null &&
    movement.quantity !== undefined
  )
})

// Show more functionality for Low Stock Items
const lowStockItemsToShow = ref(5)
const displayedLowStockItems = computed(() => {
  return lowStockItems.value.slice(0, lowStockItemsToShow.value)
})
const hasMoreLowStockItems = computed(() => {
  return lowStockItems.value.length > lowStockItemsToShow.value
})
const showLessLowStockButton = computed(() => {
  return lowStockItemsToShow.value > 5
})
const showMoreLowStock = () => {
  lowStockItemsToShow.value += 5
}
const showLessLowStock = () => {
  lowStockItemsToShow.value = 5
}

// Show more functionality for Recent Movements
const movementsToShow = ref(5)
const displayedMovements = computed(() => {
  return recentMovements.value.slice(0, movementsToShow.value)
})
const hasMoreMovements = computed(() => {
  return recentMovements.value.length > movementsToShow.value
})
const showLessMovementsButton = computed(() => {
  return movementsToShow.value > 5
})
const showMoreMovements = () => {
  movementsToShow.value += 5
}
const showLessMovements = () => {
  movementsToShow.value = 5
}

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

// Pending deliveries for awaiting_delivery requisitions
const pendingDeliveries = computed(() => {
  return store.requisitions.filter(req => 
    req.status === 'awaiting_delivery' && 
    (!req.assigned_to || req.assigned_to.toLowerCase() === currentUser.value?.username.toLowerCase())
  )
})

const awaitingDeliveryCount = computed(() => {
  return store.requisitions.filter(req => req.status === 'awaiting_delivery').length
})

// Methods
const loadDashboard = async () => {
  try {
    await store.fetchDashboardStats()
    await loadLowStockItems()
    await loadRecentMovements()
    await loadRequisitions()
  } catch (err) {
    toast.error('Failed to load dashboard data')
    console.error('Dashboard load error:', err)
  }
}

const loadRequisitions = async () => {
  try {
    await store.fetchRequisitions({ ordering: '-date_requested' })
  } catch (err) {
    console.error('Requisitions load error:', err)
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
  router.push('/in-transit')
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
    usage: 'Usage',
    waste: 'Waste'
  }
  return labels[type] || type
}

const getMovementTypeColor = (type) => {
  const colors = {
    receipt: 'bg-green-500',
    usage: 'bg-orange-500',
    waste: 'bg-red-500'
  }
  return colors[type] || 'bg-gray-500'
}

const getMovementTypeBadgeClassDark = (type) => {
  const classes = {
    receipt: 'bg-green-400 dark:bg-green-400 text-black dark:text-black',
    usage: 'bg-orange-400 dark:bg-orange-400 text-black dark:text-black',
    waste: 'bg-red-400 dark:bg-red-400 text-black dark:text-black'
  }
  return classes[type] || 'bg-gray-400 dark:bg-gray-400 text-black dark:text-black'
}

const getQuantityPrefix = (type) => {
  if (type === 'receipt') return '+'
  if (['usage', 'waste'].includes(type)) return '' // tracking only
  return ''
}

const getQuantityClassDark = (type) => {
  if (type === 'receipt') return 'text-green-400 dark:text-green-400'
  if (['usage', 'waste'].includes(type)) return 'text-orange-400 dark:text-orange-400'
  return 'text-gray-300 dark:text-gray-300'
}

const getItemCategory = (movement) => {
  const item = store.itemById(movement.item_id || movement.item?.id)
  return item?.category || ''
}

const getItemUnit = (movement) => {
  // Try to get unit from item data
  if (movement.item?.unit) return movement.item.unit
  // Fallback: try to get from items in store
  const item = store.itemById(movement.item_id)
  return item?.unit || 'units'
}

const getItemUnitForReq = (req) => {
  const item = store.itemById(req.item_id || req.item?.id)
  return item?.unit || 'units'
}

const handleQuickConfirmDelivery = async (req) => {
  try {
    // Confirm with full quantity received
    await store.confirmReceived(req.id, req.quantity_requested, '')
    toast.success('Delivery confirmed! Stock has been added.')
    await loadDashboard()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Failed to confirm delivery')
  }
}

// Lifecycle
onMounted(async () => {
  // Load user info
  try {
    const user = await getUserInfo()
    currentUser.value = user
  } catch (error) {
    console.error('Failed to get user info:', error)
  }
  
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

