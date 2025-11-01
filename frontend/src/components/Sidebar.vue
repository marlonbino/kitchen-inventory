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
      isMobileOpen || !isCollapsed ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
      collapsedWidthClass
    ]"
  >
    <div class="h-full flex flex-col bg-white dark:bg-neutral-800 border-r border-gray-200 dark:border-neutral-700 shadow-elegant">
      <!-- Logo Section -->
      <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-neutral-700 bg-gradient-to-r from-blue-50 to-white dark:from-neutral-900 dark:to-neutral-800">
        <router-link 
          to="/" 
          class="flex items-center space-x-3 group transition-transform duration-200 hover:scale-105 flex-1"
        >
          <div class="p-2 gradient-primary rounded-xl shadow-md group-hover:shadow-lg transition-shadow duration-300">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          <Transition
            enter-active-class="transition-all duration-200"
            enter-from-class="opacity-0 -translate-x-2"
            enter-to-class="opacity-100 translate-x-0"
            leave-active-class="transition-all duration-200"
            leave-from-class="opacity-100 translate-x-0"
            leave-to-class="opacity-0 -translate-x-2"
          >
            <span v-if="!isCollapsed" class="text-lg font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent hidden lg:block">
              Kitchen Inventory
            </span>
          </Transition>
        </router-link>
        
        <!-- Collapse Toggle (Desktop Only) -->
        <button
          @click="toggleCollapse"
          class="hidden lg:flex items-center justify-center p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-neutral-700 transition-colors duration-200 btn-animate"
          :aria-label="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!isCollapsed" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 overflow-y-auto custom-scrollbar py-4 px-2">
        <div class="space-y-1">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            @click="$emit('close-mobile')"
            class="group flex items-center px-3 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200 relative"
            :class="getLinkClasses(link.path)"
          >
            <!-- Icon -->
            <component :is="link.icon" class="w-5 h-5 flex-shrink-0" />
            
            <!-- Label -->
            <Transition
              enter-active-class="transition-all duration-200"
              enter-from-class="opacity-0 -translate-x-2"
              enter-to-class="opacity-100 translate-x-0"
              leave-active-class="transition-all duration-200"
              leave-from-class="opacity-100 translate-x-0"
              leave-to-class="opacity-0 -translate-x-2"
            >
              <span v-if="!isCollapsed" class="ml-3 flex-1">
                {{ link.label }}
              </span>
            </Transition>
            
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
                v-if="!isCollapsed && link.badge && link.badgeCount > 0"
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
      <div class="border-t border-gray-200 dark:border-neutral-700 p-4 space-y-2">
        <!-- Theme Toggle -->
        <button
          @click="toggleTheme"
          class="group w-full flex items-center px-3 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200 text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700"
          aria-label="Toggle dark mode"
        >
          <component :is="themeIcon" class="w-5 h-5 flex-shrink-0" />
          <Transition
            enter-active-class="transition-all duration-200"
            enter-from-class="opacity-0 -translate-x-2"
            enter-to-class="opacity-100 translate-x-0"
            leave-active-class="transition-all duration-200"
            leave-from-class="opacity-100 translate-x-0"
            leave-to-class="opacity-0 -translate-x-2"
          >
            <span v-if="!isCollapsed" class="ml-3">
              {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
            </span>
          </Transition>
        </button>

        <!-- User Info (Optional) -->
        <div
          v-if="!isCollapsed"
          class="px-3 py-2 rounded-lg bg-gradient-to-r from-blue-50 to-white dark:from-neutral-700 dark:to-neutral-800 border border-blue-100 dark:border-neutral-600"
        >
          <div class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
              <span class="text-white text-xs font-bold">AI</span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-xs font-bold text-gray-900 dark:text-white truncate">Admin User</p>
              <p class="text-xs text-gray-500 dark:text-gray-300 truncate">System Admin</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { useRoute } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'
import { useTheme } from '../composables/useTheme'

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

const SunIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z' })
])

const MoonIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': 2, d: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z' })
])

defineProps({
  isMobileOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close-mobile'])

const route = useRoute()
const store = useInventoryStore()
const { isDarkMode, toggleTheme } = useTheme()

const isCollapsed = ref(false)

const collapsedWidthClass = computed(() => {
  return isCollapsed.value ? 'lg:w-16' : 'w-64'
})

const pendingRequisitionsCount = computed(() => {
  return store.requisitions.filter(req => req.status === 'pending').length
})

const lowStockCount = computed(() => {
  return store.lowStockItems.length
})

const navLinks = computed(() => [
  {
    path: '/',
    label: 'Dashboard',
    icon: DashboardIcon,
    badge: false
  },
  {
    path: '/items',
    label: 'Items',
    icon: PackageIcon,
    badge: false
  },
  {
    path: '/movements',
    label: 'Movements',
    icon: MovementIcon,
    badge: false
  },
  {
    path: '/requisitions',
    label: 'Requisitions',
    icon: ClipboardIcon,
    badge: true,
    badgeCount: pendingRequisitionsCount.value,
    badgeColor: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-400 dark:text-black'
  },
  {
    path: '/low-stock',
    label: 'Low Stock',
    icon: AlertIcon,
    badge: true,
    badgeCount: lowStockCount.value,
    badgeColor: lowStockCount.value > 0 
      ? 'bg-red-100 text-red-800 dark:bg-red-400 dark:text-black' 
      : 'bg-gray-100 text-gray-800 dark:bg-neutral-700 dark:text-gray-300'
  }
])

const themeIcon = computed(() => {
  return isDarkMode.value ? SunIcon : MoonIcon
})

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
  localStorage.setItem('sidebarCollapsed', isCollapsed.value.toString())
}

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

// Load sidebar state from localStorage
onMounted(() => {
  const saved = localStorage.getItem('sidebarCollapsed')
  if (saved !== null) {
    isCollapsed.value = saved === 'true'
  }
})
</script>

<script>
import { onMounted } from 'vue'

export default {
  name: 'Sidebar'
}
</script>

