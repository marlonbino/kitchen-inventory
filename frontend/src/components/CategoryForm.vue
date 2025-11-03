<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <BaseInput
      v-model="formData.name"
      label="Category Name"
      placeholder="Enter category name"
      :error="errors.name"
      :required="true"
    />

    <div>
      <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        Description
      </label>
      <textarea
        id="description"
        v-model="formData.description"
        rows="3"
        placeholder="Enter category description (optional)"
        class="w-full px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white transition-colors resize-none"
      ></textarea>
      <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
    </div>

    <div class="flex justify-end gap-3 pt-4 border-t">
      <BaseButton
        variant="secondary"
        @click="$emit('cancel')"
        :disabled="loading"
      >
        Cancel
      </BaseButton>
      <BaseButton
        type="submit"
        variant="primary"
        :loading="loading"
        :disabled="loading"
      >
        {{ submitText }}
      </BaseButton>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'
import BaseInput from './BaseInput.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  category: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  submitText: {
    type: String,
    default: 'Save'
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = reactive({
  name: '',
  description: ''
})

const errors = reactive({
  name: null,
  description: null
})

// Initialize form data when category prop changes
watch(() => props.category, (newCategory) => {
  if (newCategory) {
    formData.name = newCategory.name || ''
    formData.description = newCategory.description || ''
  } else {
    // Reset form for new category
    formData.name = ''
    formData.description = ''
  }
  // Clear errors
  Object.keys(errors).forEach(key => {
    errors[key] = null
  })
}, { immediate: true })

const validateForm = () => {
  let isValid = true

  // Clear previous errors
  Object.keys(errors).forEach(key => {
    errors[key] = null
  })

  // Validate name
  if (!formData.name || formData.name.trim() === '') {
    errors.name = 'Category name is required'
    isValid = false
  }

  return isValid
}

const handleSubmit = () => {
  if (validateForm()) {
    emit('submit', { ...formData })
  }
}
</script>

<script>
export default {
  name: 'CategoryForm'
}
</script>

