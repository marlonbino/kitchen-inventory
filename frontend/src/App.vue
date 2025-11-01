<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-md">
      <NavBar />
    </header>

    <!-- Main Content -->
    <main class="flex-1">
      <router-view v-slot="{ Component, route }">
        <transition
          name="fade"
          mode="out-in"
        >
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="text-sm text-gray-600 mb-2 md:mb-0">
            © {{ currentYear }} Kitchen Inventory System. All rights reserved.
          </div>
          <div class="flex space-x-4 text-sm text-gray-600">
            <a href="#" class="hover:text-blue-600 transition-colors">Documentation</a>
            <a href="#" class="hover:text-blue-600 transition-colors">Support</a>
            <span class="text-gray-400">v1.0.0</span>
          </div>
        </div>
      </div>
    </footer>

    <!-- Global Loading Overlay -->
    <LoadingSpinner
      v-if="isLoading"
      overlay
      text="Loading..."
    />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useInventoryStore } from './stores/inventory'
import NavBar from './components/NavBar.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'

const store = useInventoryStore()

const currentYear = new Date().getFullYear()

// Check if any store is loading
const isLoading = computed(() => {
  return (
    store.loading.items ||
    store.loading.stockMovements ||
    store.loading.requisitions ||
    store.loading.dashboardStats ||
    store.loading.lowStock
  )
})

// Load initial data
onMounted(async () => {
  try {
    // Load items and low stock items in parallel
    await Promise.all([
      store.fetchItems(),
      store.fetchLowStock(),
      store.fetchRequisitions()
    ])
  } catch (error) {
    console.error('Failed to load initial data:', error)
  }
})
</script>

<style>
/* Fade transition for route changes */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
