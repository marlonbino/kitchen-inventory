<template>
  <div
    class="bg-white dark:bg-neutral-800 rounded-xl shadow-elegant p-6 transition-all duration-300 hover:shadow-elegant-lg card-hover border border-gray-100 dark:border-neutral-700"
    role="article"
    aria-labelledby="card-title"
  >
    <header v-if="title || $slots.subtitle" class="mb-4">
      <h3
        v-if="title"
        id="card-title"
        class="text-xl font-bold text-gray-900 dark:text-white tracking-tight"
      >
        {{ title }}
      </h3>
      <p
        v-if="subtitle"
        class="mt-1 text-sm text-gray-600 dark:text-gray-300 font-medium"
      >
        {{ subtitle }}
      </p>
      <div v-if="$slots.subtitle">
        <slot name="subtitle"></slot>
      </div>
    </header>
    <div class="text-gray-700 dark:text-gray-300">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: null
  },
  subtitle: {
    type: String,
    default: null
  }
})
</script>

