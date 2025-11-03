<template>
  <header class="sticky top-0 z-30 bg-white dark:bg-neutral-800 border-b border-gray-200 dark:border-neutral-700 shadow-elegant w-full max-w-full">
    <div class="px-2 sm:px-4 md:px-6 lg:px-8 w-full max-w-full">
      <div class="flex items-center justify-between h-16 w-full min-w-0">
        <!-- Left: Mobile Menu Button & Breadcrumb -->
        <div class="flex items-center space-x-4">
          <!-- Mobile Menu Toggle -->
          <button
            @click="$emit('toggle-mobile-sidebar')"
            class="lg:hidden inline-flex items-center justify-center p-2 rounded-lg text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 btn-animate"
            aria-label="Toggle sidebar"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <!-- Breadcrumb -->
          <nav class="hidden sm:flex items-center space-x-2 text-sm min-w-0 flex-1">
            <router-link
              to="/"
              class="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-white transition-colors flex-shrink-0"
            >
              Home
            </router-link>
            <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <span class="text-gray-900 dark:text-white font-medium truncate">{{ currentPageTitle }}</span>
          </nav>

          <!-- Page Title (Mobile) -->
          <h1 class="sm:hidden text-lg font-bold text-gray-900 dark:text-white truncate min-w-0">
            {{ currentPageTitle }}
          </h1>
        </div>

        <!-- Right: Actions -->
        <div class="flex items-center space-x-2 sm:space-x-3 flex-shrink-0">
          <!-- Theme Toggle (Mobile) -->
          <button
            @click="toggleTheme"
            class="lg:hidden inline-flex items-center justify-center p-2 rounded-lg text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700 transition-all duration-200 btn-animate flex-shrink-0"
            aria-label="Toggle dark mode"
          >
            <component :is="themeIcon" class="h-6 w-6" />
          </button>

          <!-- Notifications -->
          <div class="relative">
            <button
              @click="showNotifications = !showNotifications"
              class="hidden sm:inline-flex items-center justify-center p-2 rounded-lg text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700 relative transition-all duration-200 btn-animate flex-shrink-0"
              aria-label="Notifications"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span
                v-if="alertCount > 0"
                class="absolute top-1 right-1 w-2.5 h-2.5 bg-red-400 dark:bg-red-400 rounded-full border-2 border-white dark:border-neutral-800"
              ></span>
            </button>
            
            <!-- Notification Dropdown -->
            <Transition
              enter-active-class="transition-all duration-200 ease-out"
              enter-from-class="opacity-0 scale-95 translate-y-2"
              enter-to-class="opacity-100 scale-100 translate-y-0"
              leave-active-class="transition-all duration-150 ease-in"
              leave-from-class="opacity-100 scale-100 translate-y-0"
              leave-to-class="opacity-0 scale-95 translate-y-2"
            >
              <div
                v-if="showNotifications"
                class="absolute right-0 mt-2 w-80 bg-white dark:bg-neutral-800 rounded-xl shadow-elegant-lg border border-gray-200 dark:border-neutral-700 z-50 overflow-hidden"
                @click.stop
              >
                <div class="px-4 py-3 border-b border-gray-200 dark:border-neutral-700 bg-gradient-to-r from-gray-50 to-white dark:from-neutral-800 dark:to-neutral-800">
                  <div class="flex items-center justify-between">
                    <h3 class="text-sm font-bold text-gray-900 dark:text-white">Notifications</h3>
                    <button
                      @click="showNotifications = false"
                      class="text-gray-400 dark:text-gray-300 hover:text-gray-600 dark:hover:text-white transition-colors"
                      aria-label="Close notifications"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div class="max-h-96 overflow-y-auto custom-scrollbar">
                  <div v-if="notifications.length === 0" class="px-4 py-8 text-center">
                    <svg class="w-12 h-12 mx-auto text-gray-400 dark:text-gray-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                    </svg>
                    <p class="text-sm text-gray-500 dark:text-gray-400">No notifications</p>
                  </div>
                  <div v-else class="divide-y divide-gray-200 dark:divide-neutral-700">
                    <div
                      v-for="notification in notifications"
                      :key="notification.id"
                      class="px-4 py-3 hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors cursor-pointer"
                      @click="handleNotificationClick(notification)"
                    >
                      <div class="flex items-start gap-3">
                        <div :class="[
                          'w-2 h-2 rounded-full mt-2 flex-shrink-0',
                          notification.type === 'low_stock' ? 'bg-red-400 dark:bg-red-400' :
                          notification.type === 'pending' ? 'bg-yellow-400 dark:bg-yellow-400' :
                          'bg-blue-400 dark:bg-blue-400'
                        ]"></div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ notification.title }}</p>
                          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ notification.message }}</p>
                          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">{{ formatNotificationTime(notification.timestamp) }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>
          </div>

          <!-- User Menu -->
          <div class="relative hidden md:flex items-center space-x-2 lg:space-x-3 flex-shrink-0">
            <button
              @click="showUserMenu = !showUserMenu"
              class="group flex items-center space-x-3 px-3 py-2 rounded-xl transition-all duration-300 hover:shadow-lg border border-transparent hover:border-gray-200 dark:hover:border-neutral-600 bg-gradient-to-br from-gray-50/50 to-white/50 dark:from-neutral-700/50 dark:to-neutral-800/50 hover:from-gray-50 hover:to-white dark:hover:from-neutral-700 dark:hover:to-neutral-800"
            >
              <div class="hidden lg:flex flex-col items-end">
                <span class="text-sm font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {{ userName }}
                </span>
                <div class="flex items-center gap-1.5 mt-0.5">
                  <span :class="[
                    'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide transition-all',
                    roleColorClass
                  ]">
                    {{ roleLabel }}
                  </span>
                </div>
              </div>
              <div class="relative">
                <div :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center shadow-lg flex-shrink-0 transition-transform duration-300 group-hover:scale-110 group-hover:shadow-xl',
                  avatarGradientClass
                ]">
                  <span class="text-white text-sm font-bold">{{ userInitial }}</span>
                </div>
                <div :class="[
                  'absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-white dark:border-neutral-800',
                  statusDotClass
                ]"></div>
              </div>
              <svg class="w-4 h-4 text-gray-400 dark:text-gray-500 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-transform duration-300 group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            <!-- User Dropdown -->
            <Transition
              enter-active-class="transition-all duration-200 ease-out"
              enter-from-class="opacity-0 scale-95 translate-y-2"
              enter-to-class="opacity-100 scale-100 translate-y-0"
              leave-active-class="transition-all duration-150 ease-in"
              leave-from-class="opacity-100 scale-100 translate-y-0"
              leave-to-class="opacity-0 scale-95 translate-y-2"
            >
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-72 bg-white dark:bg-neutral-800 rounded-xl shadow-elegant-lg border border-gray-200 dark:border-neutral-700 z-50 overflow-hidden"
                @click.stop
              >
                <div class="px-4 py-4 border-b border-gray-200 dark:border-neutral-700 bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-700 dark:via-neutral-800 dark:to-neutral-700">
                  <div class="flex items-center space-x-3">
                    <div class="relative">
                      <div :class="[
                        'w-14 h-14 rounded-full flex items-center justify-center shadow-lg',
                        avatarGradientClass
                      ]">
                        <span class="text-white text-xl font-bold">{{ userInitial }}</span>
                      </div>
                      <div :class="[
                        'absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full border-2 border-white dark:border-neutral-800',
                        statusDotClass
                      ]"></div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <h3 class="text-base font-bold text-gray-900 dark:text-white truncate">{{ userName }}</h3>
                      <div class="flex items-center gap-2 mt-1">
                        <span :class="[
                          'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide',
                          roleColorClass
                        ]">
                          {{ roleLabel }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="py-2">
                  <button
                    @click="handleViewProfile"
                    class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-white hover:bg-gray-50 dark:hover:bg-neutral-700 transition-colors flex items-center space-x-2"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span>View Profile</span>
                  </button>
                  <div class="my-2 border-t border-gray-200 dark:border-neutral-700"></div>
                  <div class="px-4 py-2">
                    <p class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-2">System Info</p>
                    <div class="space-y-1">
                      <div class="flex justify-between text-xs text-gray-600 dark:text-gray-300">
                        <span>Account ID:</span>
                        <span class="font-mono">{{ currentUser?.id || 'N/A' }}</span>
                      </div>
                      <div class="flex justify-between text-xs text-gray-600 dark:text-gray-300">
                        <span>Email:</span>
                        <span class="truncate max-w-[120px]" :title="currentUser?.email || ''">{{ currentUser?.email || 'N/A' }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, h, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'
import { useTheme } from '../composables/useTheme'
import { getUserInfo } from '../services/api.js'

defineEmits(['toggle-mobile-sidebar'])

const route = useRoute()
const router = useRouter()
const store = useInventoryStore()
const { isDarkMode, toggleTheme } = useTheme()

const showNotifications = ref(false)
const showUserMenu = ref(false)
const notifications = ref([])
const currentUser = ref(null)

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  notifications.value = generateNotifications()
  
  // Get current user info
  try {
    const user = await getUserInfo()
    currentUser.value = user
  } catch (error) {
    console.error('Failed to get user info:', error)
  }
})

const userInitial = computed(() => {
  if (!currentUser.value?.username) return 'U'
  return currentUser.value.username.charAt(0).toUpperCase()
})

const userName = computed(() => {
  return currentUser.value?.username || 'User'
})

const roleLabel = computed(() => {
  const role = currentUser.value?.role
  if (!role) return 'User'
  return role === 'kitchen_staff' ? 'Staff' : 
         role === 'manager' ? 'Manager' : 
         'Admin'
})

const roleColorClass = computed(() => {
  const role = currentUser.value?.role
  if (role === 'admin') {
    return 'bg-gradient-to-r from-purple-500 to-purple-600 text-white shadow-md shadow-purple-500/30'
  } else if (role === 'manager') {
    return 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md shadow-blue-500/30'
  } else {
    return 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-md shadow-green-500/30'
  }
})

const avatarGradientClass = computed(() => {
  const role = currentUser.value?.role
  if (role === 'admin') {
    return 'bg-gradient-to-br from-purple-500 to-purple-700'
  } else if (role === 'manager') {
    return 'bg-gradient-to-br from-blue-500 to-blue-700'
  } else {
    return 'bg-gradient-to-br from-green-500 to-green-700'
  }
})

const statusDotClass = computed(() => {
  // Always show as online (green dot)
  return 'bg-green-400 dark:bg-green-500'
})

const handleViewProfile = () => {
  // Future: Add profile page
  showUserMenu.value = false
}

const currentPageTitle = computed(() => {
  return route.meta.title || 'Dashboard'
})

const alertCount = computed(() => {
  return store.lowStockItems.length + store.requisitions.filter(req => req.status === 'pending').length
})

// Generate notifications from store data
const generateNotifications = () => {
  const newNotifications = []
  
  // Low stock notifications
  store.lowStockItems.forEach((item, index) => {
    if (item.current_stock === 0) {
      newNotifications.push({
        id: `low-stock-${item.id}`,
        type: 'low_stock',
        title: 'Out of Stock Alert',
        message: `${item.name} is out of stock`,
        timestamp: new Date(),
        action: { type: 'navigate', path: '/low-stock' }
      })
    } else {
      newNotifications.push({
        id: `low-stock-${item.id}`,
        type: 'low_stock',
        title: 'Low Stock Alert',
        message: `${item.name} is running low (${item.current_stock} ${item.unit})`,
        timestamp: new Date(),
        action: { type: 'navigate', path: '/low-stock' }
      })
    }
  })
  
  // Pending requisitions notifications
  store.requisitions
    .filter(req => req.status === 'pending')
    .slice(0, 5) // Limit to 5 most recent
    .forEach(req => {
      newNotifications.push({
        id: `pending-${req.id}`,
        type: 'pending',
        title: 'Pending Requisition',
        message: `${req.item_name || 'Item'} requested by ${req.requested_by}`,
        timestamp: new Date(req.date_requested),
        action: { type: 'navigate', path: '/requisitions' }
      })
    })
  
  // Sort by timestamp (newest first)
  newNotifications.sort((a, b) => b.timestamp - a.timestamp)
  
  return newNotifications.slice(0, 10) // Keep only 10 most recent
}

// Update notifications when store data changes
watch([() => store.lowStockItems, () => store.requisitions], () => {
  notifications.value = generateNotifications()
}, { deep: true, immediate: true })

// Handle notification click
const handleNotificationClick = (notification) => {
  if (notification.action?.type === 'navigate') {
    router.push(notification.action.path)
    showNotifications.value = false
  }
}

// Format notification time
const formatNotificationTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}

// Close dropdowns when clicking outside
const handleClickOutside = (event) => {
  const notificationElement = event.target.closest('.relative')
  const userMenuElement = event.target.closest('.relative')
  
  if (showNotifications.value && !notificationElement) {
    showNotifications.value = false
  }
  if (showUserMenu.value && !userMenuElement?.querySelector('button')) {
    showUserMenu.value = false
  }
}

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const SunIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z' })
])

const MoonIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z' })
])

const themeIcon = computed(() => {
  return isDarkMode.value ? SunIcon : MoonIcon
})
</script>
