<template>
  <nav class="bg-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo and Title -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-3">
            <div class="p-2 bg-blue-600 rounded-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
            <span class="text-xl font-bold text-gray-900 hidden sm:block">Kitchen Inventory</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex md:items-center md:space-x-1">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 relative"
            :class="isActive(link.path) ? 'bg-blue-50 text-blue-600' : 'text-gray-700 hover:bg-gray-100'"
          >
            {{ link.label }}
            <span
              v-if="link.badge && link.badgeCount > 0"
              class="absolute -top-1 -right-1 px-1.5 py-0.5 text-xs font-medium rounded-full"
              :class="link.badgeColor"
            >
              {{ link.badgeCount > 99 ? '99+' : link.badgeCount }}
            </span>
          </router-link>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Toggle menu"
          >
            <svg
              v-if="!mobileMenuOpen"
              class="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg
              v-else
              class="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation Menu -->
    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 relative"
            :class="isActive(link.path) ? 'bg-blue-50 text-blue-600' : 'text-gray-700 hover:bg-gray-100'"
          >
            <div class="flex items-center justify-between">
              <span>{{ link.label }}</span>
              <span
                v-if="link.badge && link.badgeCount > 0"
                class="px-2 py-0.5 text-xs font-medium rounded-full"
                :class="link.badgeColor"
              >
                {{ link.badgeCount > 99 ? '99+' : link.badgeCount }}
              </span>
            </div>
          </router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useInventoryStore } from '../stores/inventory'

const route = useRoute()
const store = useInventoryStore()
const mobileMenuOpen = ref(false)

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
    badge: false
  },
  {
    path: '/items',
    label: 'Items',
    badge: false
  },
  {
    path: '/movements',
    label: 'Movements',
    badge: false
  },
  {
    path: '/requisitions',
    label: 'Requisitions',
    badge: true,
    badgeCount: pendingRequisitionsCount.value,
    badgeColor: 'bg-yellow-100 text-yellow-800'
  },
  {
    path: '/low-stock',
    label: 'Low Stock',
    badge: true,
    badgeCount: lowStockCount.value,
    badgeColor: lowStockCount.value > 0 ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
  }
])

const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>

