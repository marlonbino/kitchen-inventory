<template>
  <div
    class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full font-bold text-sm"
    :class="badgeClasses"
    :title="tooltipText"
    role="status"
    :aria-label="ariaLabel"
  >
    <span class="font-bold">{{ current }}</span>
    <span class="font-bold">/</span>
    <span class="font-bold">{{ minimum }}</span>
    <span
      v-if="showPercentage"
      class="ml-1 text-xs opacity-75"
    >
      ({{ percentage }}%)
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  current: {
    type: Number,
    required: true,
    validator: (value) => value >= 0
  },
  minimum: {
    type: Number,
    required: true,
    validator: (value) => value > 0
  },
  showPercentage: {
    type: Boolean,
    default: false
  }
})

const percentage = computed(() => {
  const percent = (props.current / props.minimum) * 100
  return Math.round(percent)
})

const status = computed(() => {
  if (props.current < props.minimum) {
    return 'low' // Red - below minimum
  } else if (props.current < props.minimum * 1.5) {
    return 'warning' // Yellow - below 1.5x minimum
  } else {
    return 'good' // Green - above 1.5x minimum
  }
})

const badgeClasses = computed(() => {
  const baseClasses = 'transition-colors duration-200'
  
  const statusClasses = {
    low: 'bg-red-100 dark:bg-red-400 text-red-800 dark:text-black',
    warning: 'bg-yellow-100 dark:bg-yellow-400 text-yellow-800 dark:text-black',
    good: 'bg-green-100 dark:bg-green-400 text-green-800 dark:text-black'
  }
  
  return `${baseClasses} ${statusClasses[status.value]}`
})

const tooltipText = computed(() => {
  const statusText = {
    low: 'Low stock - below minimum level',
    warning: 'Warning - stock is low',
    good: 'Stock level is adequate'
  }
  
  return `${statusText[status.value]}. Current: ${props.current}, Minimum: ${props.minimum}`
})

const ariaLabel = computed(() => {
  return `Stock level: ${props.current} out of ${props.minimum} (${status.value === 'low' ? 'low' : status.value === 'warning' ? 'warning' : 'adequate'})`
})
</script>

