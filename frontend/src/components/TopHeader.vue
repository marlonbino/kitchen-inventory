<template>
  <header class="sticky top-0 z-30 bg-white dark:bg-neutral-800 border-b border-gray-200 dark:border-neutral-700 shadow-elegant">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
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
          <nav class="hidden sm:flex items-center space-x-2 text-sm">
            <router-link
              to="/"
              class="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-white transition-colors"
            >
              Home
            </router-link>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <span class="text-gray-900 dark:text-white font-medium">{{ currentPageTitle }}</span>
          </nav>

          <!-- Page Title (Mobile) -->
          <h1 class="sm:hidden text-lg font-bold text-gray-900 dark:text-white">
            {{ currentPageTitle }}
          </h1>
        </div>

        <!-- Right: Actions -->
        <div class="flex items-center space-x-3">
          <!-- Theme Toggle (Mobile) -->
          <button
            @click="toggleTheme"
            class="lg:hidden inline-flex items-center justify-center p-2 rounded-lg text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700 transition-all duration-200 btn-animate"
            aria-label="Toggle dark mode"
          >
            <component :is="themeIcon" class="h-6 w-6" />
          </button>

          <!-- Notifications (Optional) -->
          <button
            class="hidden sm:inline-flex items-center justify-center p-2 rounded-lg text-gray-700 dark:text-white hover:bg-gray-100 dark:hover:bg-neutral-700 relative transition-all duration-200 btn-animate"
            aria-label="Notifications"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span
              v-if="alertCount > 0"
              class="absolute top-1 right-1 w-2.5 h-2.5 bg-red-400 dark:bg-red-400 rounded-full"
            ></span>
          </button>

          <!-- User Menu (Optional) -->
          <div class="hidden md:flex items-center space-x-3">
            <div class="flex flex-col items-end">
              <span class="text-sm font-semibold text-gray-900 dark:text-white">Admin User</span>
              <span class="text-xs text-gray-500 dark:text-gray-300">System Admin</span>
            </div>
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-md">
              <span class="text-white text-sm font-bold">AI</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, h } from 'vue'
import { useRoute } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'
import { useTheme } from '../composables/useTheme'

defineEmits(['toggle-mobile-sidebar'])

const route = useRoute()
const store = useInventoryStore()
const { isDarkMode, toggleTheme } = useTheme()

const currentPageTitle = computed(() => {
  return route.meta.title || 'Dashboard'
})

const alertCount = computed(() => {
  return store.lowStockItems.length + store.requisitions.filter(req => req.status === 'pending').length
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

