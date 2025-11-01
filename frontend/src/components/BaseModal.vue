<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="show"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click.self="handleClose"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="titleId"
      >
        <!-- Backdrop -->
        <div
          class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
          aria-hidden="true"
        ></div>

        <!-- Modal container -->
        <div class="flex min-h-full items-center justify-center p-4">
          <div
            class="relative bg-white dark:bg-neutral-800 rounded-2xl shadow-elegant-lg max-w-md w-full mx-auto transform transition-all border border-gray-100 dark:border-neutral-700 overflow-hidden"
            @click.stop
          >
            <!-- Header -->
            <div
              v-if="title || $slots.header"
              class="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-neutral-700 bg-gradient-to-r from-gray-50 to-white dark:from-neutral-800 dark:to-neutral-800"
            >
              <div class="flex-1">
                <h2
                  v-if="title"
                  :id="titleId"
                  class="text-xl font-bold text-gray-900 dark:text-white"
                >
                  {{ title }}
                </h2>
                <slot name="header"></slot>
              </div>
              <button
                v-if="closable"
                @click="handleClose"
                class="ml-4 text-gray-400 dark:text-gray-300 hover:text-gray-600 dark:hover:text-white focus:outline-none focus:text-gray-600 dark:focus:text-white transition-all duration-200 hover:bg-gray-100 dark:hover:bg-neutral-700 rounded-lg p-1 btn-animate"
                aria-label="Close modal"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <!-- Content -->
            <div class="px-6 py-5 max-h-[calc(100vh-200px)] overflow-y-auto custom-scrollbar">
              <slot></slot>
            </div>

            <!-- Footer -->
            <div
              v-if="$slots.footer"
              class="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-100 dark:border-neutral-700 bg-gradient-to-br from-gray-50 to-white dark:from-neutral-800 dark:to-neutral-800 rounded-b-2xl"
            >
              <slot name="footer"></slot>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: null
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close', 'update:show'])

// Generate unique ID for title
const titleId = computed(() => `modal-title-${Math.random().toString(36).substr(2, 9)}`)

const handleClose = () => {
  if (props.closable) {
    emit('close')
    emit('update:show', false)
  }
}

// Handle ESC key
const handleEscape = (event) => {
  if (event.key === 'Escape' && props.show && props.closable) {
    handleClose()
  }
}

// Focus management - focus first focusable element when modal opens
const focusFirstElement = () => {
  if (props.show) {
    nextTick(() => {
      const modal = document.querySelector('[role="dialog"]')
      if (modal) {
        const focusableElements = modal.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        if (focusableElements.length > 0) {
          focusableElements[0].focus()
        }
      }
    })
  }
}

// Handle body scroll lock
const lockBodyScroll = () => {
  document.body.style.overflow = 'hidden'
}

const unlockBodyScroll = () => {
  document.body.style.overflow = ''
}

// Watch show prop to manage scroll lock and focus
watch(() => props.show, (newValue) => {
  if (newValue) {
    lockBodyScroll()
    focusFirstElement()
  } else {
    unlockBodyScroll()
  }
})

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
  if (props.show) {
    lockBodyScroll()
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  unlockBodyScroll()
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white,
.modal-enter-active .dark\:bg-neutral-800,
.modal-leave-active .dark\:bg-neutral-800 {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white,
.modal-enter-from .dark\:bg-neutral-800,
.modal-leave-to .dark\:bg-neutral-800 {
  opacity: 0;
  transform: scale(0.95) translateY(-20px);
}

/* Backdrop blur effect */
.modal-enter-active .fixed.inset-0,
.modal-leave-active .fixed.inset-0 {
  transition: opacity 0.25s ease, backdrop-filter 0.25s ease;
}

.modal-enter-from .fixed.inset-0,
.modal-leave-to .fixed.inset-0 {
  backdrop-filter: blur(0);
}
</style>

