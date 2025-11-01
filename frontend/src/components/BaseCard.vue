<template>
  <div
    class="bg-white rounded-lg shadow-md p-6 transition-shadow hover:shadow-lg"
    role="article"
    aria-labelledby="card-title"
  >
    <header v-if="title || $slots.subtitle" class="mb-4">
      <h3
        v-if="title"
        id="card-title"
        class="text-xl font-semibold text-gray-800"
      >
        {{ title }}
      </h3>
      <p
        v-if="subtitle"
        class="mt-1 text-sm text-gray-600"
      >
        {{ subtitle }}
      </p>
      <div v-if="$slots.subtitle">
        <slot name="subtitle"></slot>
      </div>
    </header>
    <div class="text-gray-700">
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

