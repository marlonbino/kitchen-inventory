<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    :aria-busy="loading"
    :aria-disabled="disabled || loading"
    @click="handleClick"
    type="button"
  >
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      ></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    <slot></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const buttonClasses = computed(() => {
  const baseClasses = 'inline-flex items-center justify-center px-5 py-2.5 rounded-lg font-semibold text-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-neutral-800 disabled:opacity-50 disabled:cursor-not-allowed btn-animate shadow-sm hover:shadow-md'
  
  const variantClasses = {
    primary: 'bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-500 text-white hover:from-blue-600 hover:to-blue-700 dark:hover:from-blue-500 dark:hover:to-blue-600 focus:ring-blue-500 shadow-blue-100 dark:shadow-blue-900/50',
    secondary: 'bg-gray-100 dark:bg-neutral-700 text-gray-700 dark:text-white hover:bg-gray-200 dark:hover:bg-neutral-600 focus:ring-gray-400 dark:focus:ring-gray-500 border border-gray-200 dark:border-neutral-600',
    danger: 'bg-gradient-to-r from-red-500 to-red-600 dark:from-red-600 dark:to-red-500 text-white hover:from-red-600 hover:to-red-700 dark:hover:from-red-500 dark:hover:to-red-600 focus:ring-red-500 shadow-red-100 dark:shadow-red-900/50'
  }
  
  return `${baseClasses} ${variantClasses[props.variant]}`
})

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

