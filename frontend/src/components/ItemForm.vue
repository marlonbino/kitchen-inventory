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
      v-model="formData.supplier"
      label="Supplier/Vendor (Optional)"
      placeholder="e.g., Ngara Market"
      :error="errors.supplier"
    />

    <BaseInput
      v-if="isAdmin"
      v-model.number="formData.price_per_unit"
      type="number"
      step="0.01"
      label="Price Per Unit in KES (Optional)"
      placeholder="0.00"
      :error="errors.price_per_unit"
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
import { ref, reactive, watch, computed, onMounted } from 'vue'
import BaseInput from './BaseInput.vue'
import BaseSelect from './BaseSelect.vue'
import BaseButton from './BaseButton.vue'
import { getCategories, getUserInfo } from '../services/api.js'

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

// Check if user is admin for price field visibility
const isAdmin = ref(false)
onMounted(async () => {
  try {
    const user = await getUserInfo()
    isAdmin.value = user.role === 'admin'
  } catch (error) {
    console.error('Failed to get user info:', error)
  }
  loadCategories()
})

const categoryOptions = ref([
  { value: '', label: 'Loading categories...' }
])

const unitOptions = [
  { value: 'kg', label: 'Kilogram (Kg)' },
  { value: 'litre', label: 'Litre (L)' },
  { value: 'piece', label: 'Piece' },
  { value: 'packet', label: 'Packet' },
  { value: 'dozen', label: 'Dozen' },
  { value: 'bale', label: 'Bale' }
]

const formData = reactive({
  name: '',
  category: '',
  unit: '',
  supplier: '',
  price_per_unit: null,
  min_stock_level: 0
})

const errors = reactive({
  name: null,
  category: null,
  unit: null,
  supplier: null,
  price_per_unit: null,
  min_stock_level: null
})

// Load categories from API
const loadCategories = async () => {
  try {
    const categories = await getCategories()
    categoryOptions.value = categories.map(cat => ({
      value: cat.id,
      label: cat.name
    }))
  } catch (error) {
    console.error('Error loading categories:', error)
    // Keep default categories as fallback
    categoryOptions.value = [
      { value: '', label: 'Select category...' }
    ]
  }
}

// Initialize form data when item prop changes
watch(() => props.item, (newItem) => {
  if (newItem) {
    formData.name = newItem.name || ''
    formData.category = newItem.category || ''  // This will be the category ID now
    formData.unit = newItem.unit || ''
    formData.supplier = newItem.supplier || ''
    formData.price_per_unit = newItem.price_per_unit || null
    formData.min_stock_level = newItem.min_stock_level || 0
  } else {
    // Reset form for new item
    formData.name = ''
    formData.category = ''
    formData.unit = ''
    formData.supplier = ''
    formData.price_per_unit = null
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

  // Validate price if provided
  if (formData.price_per_unit !== null && formData.price_per_unit !== undefined) {
    if (formData.price_per_unit < 0) {
      errors.price_per_unit = 'Price must be greater than or equal to 0'
      isValid = false
    }
  }

  return isValid
}

const handleSubmit = () => {
  if (validateForm()) {
    emit('submit', { ...formData })
  }
}
</script>

