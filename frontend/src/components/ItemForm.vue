<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <BaseInput
      v-model="formData.name"
      label="Item Name"
      placeholder="Enter item name"
      :error="errors.name"
      :required="true"
    />

    <BaseSelect
      v-model="formData.category"
      label="Category"
      :options="categoryOptions"
      :error="errors.category"
      :required="true"
    />

    <BaseSelect
      v-model="formData.unit"
      label="Unit"
      :options="unitOptions"
      :error="errors.unit"
      :required="true"
    />

    <BaseInput
      v-model.number="formData.min_stock_level"
      type="number"
      label="Minimum Stock Level"
      placeholder="0"
      :error="errors.min_stock_level"
      :required="true"
    />

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
import { ref, reactive, watch, computed } from 'vue'
import BaseInput from './BaseInput.vue'
import BaseSelect from './BaseSelect.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  item: {
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

const categoryOptions = [
  { value: 'Produce', label: 'Produce' },
  { value: 'Dairy', label: 'Dairy' },
  { value: 'Pantry', label: 'Pantry' },
  { value: 'Meat', label: 'Meat' },
  { value: 'Spices', label: 'Spices' },
  { value: 'Frozen', label: 'Frozen' },
  { value: 'Other', label: 'Other' }
]

const unitOptions = [
  { value: 'kg', label: 'Kilogram' },
  { value: 'g', label: 'Gram' },
  { value: 'lb', label: 'Pound' },
  { value: 'oz', label: 'Ounce' },
  { value: 'piece', label: 'Piece' },
  { value: 'bottle', label: 'Bottle' },
  { value: 'pack', label: 'Pack' }
]

const formData = reactive({
  name: '',
  category: '',
  unit: '',
  min_stock_level: 0
})

const errors = reactive({
  name: null,
  category: null,
  unit: null,
  min_stock_level: null
})

// Initialize form data when item prop changes
watch(() => props.item, (newItem) => {
  if (newItem) {
    formData.name = newItem.name || ''
    formData.category = newItem.category || ''
    formData.unit = newItem.unit || ''
    formData.min_stock_level = newItem.min_stock_level || 0
  } else {
    // Reset form for new item
    formData.name = ''
    formData.category = ''
    formData.unit = ''
    formData.min_stock_level = 0
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
    errors.name = 'Item name is required'
    isValid = false
  }

  // Validate category
  if (!formData.category) {
    errors.category = 'Category is required'
    isValid = false
  }

  // Validate unit
  if (!formData.unit) {
    errors.unit = 'Unit is required'
    isValid = false
  }

  // Validate min_stock_level
  if (formData.min_stock_level === null || formData.min_stock_level === undefined) {
    errors.min_stock_level = 'Minimum stock level is required'
    isValid = false
  } else if (formData.min_stock_level < 0) {
    errors.min_stock_level = 'Minimum stock level must be greater than or equal to 0'
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

