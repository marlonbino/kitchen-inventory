<template>
  <div class="text-center py-12">
    <!-- Icon -->
    <div class="flex justify-center">
      <div
        class="rounded-full p-4"
        :class="iconBgClass"
      >
        <component
          :is="iconComponent"
          :class="['h-12 w-12', iconColorClass]"
        />
      </div>
    </div>

    <!-- Title -->
    <h3 class="mt-6 text-xl font-semibold text-gray-900">{{ title }}</h3>

    <!-- Message -->
    <p class="mt-2 text-gray-600 max-w-md mx-auto">{{ message }}</p>

    <!-- Action Button -->
    <div v-if="actionText" class="mt-6">
      <router-link v-if="actionLink" :to="actionLink">
        <BaseButton variant="primary">
          {{ actionText }}
        </BaseButton>
      </router-link>
      <BaseButton v-else variant="primary" @click="$emit('action')">
        {{ actionText }}
      </BaseButton>
    </div>

    <!-- Custom Slot -->
    <div v-if="$slots.default" class="mt-6">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  icon: {
    type: String,
    default: 'box',
    validator: (value) => ['box', 'check', 'warning', 'search', 'inbox', 'folder'].includes(value)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  actionText: {
    type: String,
    default: null
  },
  actionLink: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['action'])

const iconComponent = computed(() => {
  const icons = {
    box: () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4'
      })
    ]),
    check: () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
      })
    ]),
    warning: () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
      })
    ]),
    search: () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'
      })
    ]),
    inbox: () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4'
      })
    ]),
    folder: () => h('svg', {
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24'
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z'
      })
    ])
  }
  return icons[props.icon] || icons.box
})

const iconBgClass = computed(() => {
  const classes = {
    box: 'bg-gray-100',
    check: 'bg-green-100',
    warning: 'bg-yellow-100',
    search: 'bg-blue-100',
    inbox: 'bg-purple-100',
    folder: 'bg-indigo-100'
  }
  return classes[props.icon] || classes.box
})

const iconColorClass = computed(() => {
  const classes = {
    box: 'text-gray-600',
    check: 'text-green-600',
    warning: 'text-yellow-600',
    search: 'text-blue-600',
    inbox: 'text-purple-600',
    folder: 'text-indigo-600'
  }
  return classes[props.icon] || classes.box
})
</script>

