<template>
  <nav class="bg-white shadow-elegant sticky top-0 z-50 border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo and Title -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2 group transition-transform duration-200 hover:scale-105">
            <img :src="bitzLogo" alt="BITZ Logo" class="h-10 w-auto">
            <span class="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent hidden sm:block">Kitchen</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex md:items-center md:space-x-2">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 relative overflow-hidden group"
            :class="isActive(link.path) 
              ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-md' 
              : 'text-gray-700 hover:bg-gray-50'"
          >
            <span class="relative z-10">{{ link.label }}</span>
            <div v-if="!isActive(link.path)" class="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-600 opacity-0 group-hover:opacity-5 transition-opacity duration-200"></div>
            <span
              v-if="link.badge && link.badgeCount > 0"
              class="absolute -top-1 -right-1 px-2 py-0.5 text-xs font-bold rounded-full shadow-sm"
              :class="isActive(link.path) ? 'bg-white text-blue-600' : link.badgeColor"
            >
              {{ link.badgeCount > 99 ? '99+' : link.badgeCount }}
            </span>
          </router-link>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-lg text-gray-700 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 btn-animate"
            aria-label="Toggle menu"
          >
            <svg
              v-if="!mobileMenuOpen"
              class="h-6 w-6 transition-transform duration-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg
              v-else
              class="h-6 w-6 transition-transform duration-200 rotate-90"
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
      enter-active-class="transition ease-out duration-200"
      enter-from-class="transform opacity-0 -translate-y-2"
      enter-to-class="transform opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 translate-y-0"
      leave-to-class="transform opacity-0 -translate-y-2"
    >
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-100 bg-gradient-to-b from-white to-gray-50">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            @click="mobileMenuOpen = false"
            class="block px-4 py-3 rounded-lg text-base font-semibold transition-all duration-200 relative overflow-hidden group"
            :class="isActive(link.path) 
              ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md' 
              : 'text-gray-700 hover:bg-gray-50'"
          >
            <div class="flex items-center justify-between relative z-10">
              <span>{{ link.label }}</span>
              <span
                v-if="link.badge && link.badgeCount > 0"
                class="px-2.5 py-1 text-xs font-bold rounded-full shadow-sm"
                :class="isActive(link.path) ? 'bg-white text-blue-600' : link.badgeColor"
              >
                {{ link.badgeCount > 99 ? '99+' : link.badgeCount }}
              </span>
            </div>
            <div v-if="!isActive(link.path)" class="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-600 opacity-0 group-hover:opacity-5 transition-opacity duration-200"></div>
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
import bitzLogo from '../assets/bitz-logo.svg'

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

