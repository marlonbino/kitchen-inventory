<template>
  <!-- Mobile Overlay -->
  <Transition
    enter-active-class="transition-opacity duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-300"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="isMobileOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
      @click="$emit('close-mobile')"
    ></div>
  </Transition>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed lg:static inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out',
      isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
    ]"
    style="max-width: 100vw;"
  >
    <div class="h-full flex flex-col bg-white dark:bg-neutral-800 border-r border-gray-200 dark:border-neutral-700 shadow-elegant overflow-hidden">
      <!-- Logo Section -->
      <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-neutral-700 bg-gradient-to-r from-blue-50 to-white dark:from-neutral-900 dark:to-neutral-800 flex-shrink-0">
          <router-link 
          to="/" 
          class="flex items-center space-x-2 group transition-transform duration-200 hover:scale-105 flex-1 min-w-0"
        >
          <img :src="bitzLogo" alt="BITZ Logo" class="h-10 w-auto flex-shrink-0 brightness-0 dark:brightness-100 invert dark:invert-0">
          <span class="text-lg font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent truncate hidden sm:block">
            Kitchen
          </span>
        </router-link>
        
        <!-- Close Button (Mobile Only) -->
        <button
          @click="$emit('close-mobile')"
          class="lg:hidden inline-flex items-center justify-center p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-neutral-700 transition-colors duration-200 btn-animate flex-shrink-0 ml-2"
          aria-label="Close sidebar"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 overflow-hidden py-4 px-2 min-h-0">
        <div class="flex flex-col justify-evenly h-full overflow-y-auto custom-scrollbar gap-2">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            @click="$emit('close-mobile')"
            class="group flex items-center px-3 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200 relative flex-shrink-0"
            :class="getLinkClasses(link.path)"
          >
            <!-- Icon -->
            <component :is="link.icon" class="w-5 h-5 flex-shrink-0" />
            
            <!-- Label -->
            <span class="ml-3 flex-1 whitespace-nowrap">
              {{ link.label }}
            </span>
            
            <!-- Badge -->
            <Transition
              enter-active-class="transition-all duration-200"
              enter-from-class="opacity-0 scale-75"
              enter-to-class="opacity-100 scale-100"
              leave-active-class="transition-all duration-200"
              leave-from-class="opacity-100 scale-100"
              leave-to-class="opacity-0 scale-75"
            >
              <span
                v-if="link.badge && link.badgeCount > 0"
                class="ml-auto px-2 py-0.5 text-xs font-bold rounded-full"
                :class="getBadgeClasses(link.path)"
              >
                {{ link.badgeCount > 99 ? '99+' : link.badgeCount }}
              </span>
            </Transition>

            <!-- Active Indicator -->
            <Transition
              enter-active-class="transition-transform duration-200"
              enter-from-class="scale-x-0"
              enter-to-class="scale-x-100"
              leave-active-class="transition-transform duration-200"
              leave-from-class="scale-x-100"
              leave-to-class="scale-x-0"
            >
              <div
                v-if="isActive(link.path)"
                class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-blue-500 to-blue-600 rounded-r-full"
              ></div>
            </Transition>
          </router-link>
        </div>
      </nav>

      <!-- Bottom Section -->
      <div class="border-t border-gray-200 dark:border-neutral-700 p-4 space-y-2 flex-shrink-0">
        <!-- Theme Toggle -->
        <button
          @click="toggleTheme"
          class="group w-full flex items-center px-3 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200 text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700"
          aria-label="Toggle dark mode"
        >
          <component :is="themeIcon" class="w-5 h-5 flex-shrink-0" />
          <span class="ml-3 whitespace-nowrap">
            {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
          </span>
        </button>

        <!-- Logout Button -->
        <button
          @click="handleLogout"
          class="group w-full flex items-center px-3 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
        >
          <component :is="LogoutIcon" class="w-5 h-5 flex-shrink-0" />
          <span class="ml-3 whitespace-nowrap">Logout</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, h, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'
import { useTheme } from '../composables/useTheme'
import { logout as apiLogout, getUserInfo } from '../services/api.js'
import bitzLogo from '../assets/bitz-logo.svg'

// Define SVG icons as components
const DashboardIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
])

const PackageIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' })
])

const MovementIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4' })
])

const ClipboardIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
])

const AlertIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
])

const FolderIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z' })
])

const UsersIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z' })
])

const ChartIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])

const SunIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z' })
])

const MoonIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z' })
])

const LogoutIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1' })
])

defineProps({
  isMobileOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close-mobile'])

const route = useRoute()
const router = useRouter()
const store = useInventoryStore()
const { isDarkMode, toggleTheme } = useTheme()

const currentUser = ref(null)

onMounted(async () => {
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

const handleLogout = async () => {
  try {
    await apiLogout()
    localStorage.removeItem('user')
    localStorage.removeItem('auth_token')
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
    // Still redirect to login even if logout API fails
    localStorage.removeItem('user')
    localStorage.removeItem('auth_token')
    router.push('/login')
  }
}

const pendingRequisitionsCount = computed(() => {
  return store.requisitions.filter(req => req.status === 'pending').length
})

const inTransitCount = computed(() => {
  return store.requisitions.filter(req => req.status === 'awaiting_delivery').length
})

const lowStockCount = computed(() => {
  return store.lowStockItems.length
})

const isAdmin = computed(() => currentUser.value?.role === 'admin')

const navLinks = computed(() => {
  const links = [
    {
      path: '/',
      label: 'Dashboard',
      icon: DashboardIcon,
      badge: false
    },
    {
      path: '/items',
      label: 'Inventory Items',
      icon: PackageIcon,
      badge: false
    },
    {
      path: '/movements',
      label: 'Stock Usage',
      icon: MovementIcon,
      badge: false
    },
    {
      path: '/requisitions',
      label: 'Purchase Requests',
      icon: ClipboardIcon,
      badge: true,
      badgeCount: pendingRequisitionsCount.value,
      badgeColor: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-400 dark:text-black'
    },
    {
      path: '/low-stock',
      label: 'Low Stock Alert',
      icon: AlertIcon,
      badge: true,
      badgeCount: lowStockCount.value,
      badgeColor: lowStockCount.value > 0 
        ? 'bg-red-100 text-red-800 dark:bg-red-400 dark:text-black' 
        : 'bg-gray-100 text-gray-800 dark:bg-neutral-700 dark:text-gray-300'
    },
    {
      path: '/in-transit',
      label: 'Pending Deliveries',
      icon: ClipboardIcon,
      badge: true,
      badgeCount: inTransitCount.value,
      badgeColor: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-400 dark:text-black'
    },
    {
      path: '/analytics',
      label: 'Analytics & Reports',
      icon: ChartIcon,
      badge: false
    }
  ]
  
  // Add admin-only links
  if (isAdmin.value) {
    links.push({
      path: '/categories',
      label: 'Manage Categories',
      icon: FolderIcon,
      badge: false
    })
    links.push({
      path: '/users',
      label: 'Manage Users',
      icon: UsersIcon,
      badge: false
    })
  }
  
  return links
})

const themeIcon = computed(() => {
  return isDarkMode.value ? SunIcon : MoonIcon
})

const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

const getLinkClasses = (path) => {
  if (isActive(path)) {
    return 'bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-500 text-white shadow-md'
  }
  return 'text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700'
}

const getBadgeClasses = (path) => {
  if (isActive(path)) {
    return 'bg-white text-blue-600 dark:bg-neutral-900 dark:text-blue-400'
  }
  const link = navLinks.value.find(l => l.path === path)
  return link?.badgeColor || 'bg-gray-100 text-gray-800 dark:bg-neutral-700 dark:text-gray-300'
}

</script>

<script>
export default {
  name: 'Sidebar'
}
</script>

