<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <EmptyState
      icon="search"
      title="Page Not Found"
      message="The page you're looking for doesn't exist or has been moved."
      action-text="Go to Dashboard"
      action-link="/"
    />
  </div>
</template>

<script setup>
import EmptyState from '../components/EmptyState.vue'
</script>

