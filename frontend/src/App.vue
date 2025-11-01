<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-neutral-900">
    <!-- Sidebar + Main Layout -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <Sidebar :is-mobile-open="isMobileSidebarOpen" @close-mobile="isMobileSidebarOpen = false" />
      
      <!-- Main Content Area -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Top Header -->
        <TopHeader @toggle-mobile-sidebar="isMobileSidebarOpen = !isMobileSidebarOpen" />
        
        <!-- Page Content -->
        <main class="flex-1 overflow-y-auto bg-gray-50 dark:bg-neutral-900">
          <router-view v-slot="{ Component, route }">
            <transition
              name="fade-slide"
              mode="out-in"
            >
              <component :is="Component" :key="route.path" />
            </transition>
          </router-view>
        </main>
      </div>
    </div>

    <!-- Global Loading Overlay -->
    <LoadingSpinner
      v-if="isLoading"
      overlay
      text="Loading..."
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from './stores/inventory'
import { useTheme } from './composables/useTheme'
import Sidebar from './components/Sidebar.vue'
import TopHeader from './components/TopHeader.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'

const store = useInventoryStore()
const { initTheme } = useTheme()

const isMobileSidebarOpen = ref(false)

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
  // Initialize theme
  initTheme()
  
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
/* Enhanced fade-slide transition for route changes */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Professional custom scrollbar - Light mode */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #f8fafc;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #cbd5e1 0%, #94a3b8 100%);
  border-radius: 5px;
  transition: all 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #94a3b8 0%, #64748b 100%);
}

/* Dark mode scrollbar */
.dark ::-webkit-scrollbar-track {
  background: #262626;
  border-radius: 5px;
}

.dark ::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #525252 0%, #404040 100%);
  border-radius: 5px;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #6b6b6b 0%, #525252 100%);
}

/* Prevent layout shift on transition */
main {
  position: relative;
}
</style>
