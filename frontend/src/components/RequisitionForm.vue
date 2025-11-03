<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <BaseSelect
      v-model="formData.item_id"
      label="Item"
      :options="sortedItemOptions"
      :error="errors.item_id"
      :required="true"
      placeholder="Select an item..."
    />

    <!-- Item Info Display -->
    <div v-if="selectedItem" class="p-3 bg-blue-50 border border-blue-200 rounded-md">
      <div class="grid grid-cols-2 gap-2 text-sm">
        <div>
          <span class="text-blue-700 font-medium">Current Stock:</span>
          <span class="ml-2 text-blue-900">{{ selectedItem.current_stock }} {{ selectedItem.unit }}</span>
        </div>
        <div>
          <span class="text-blue-700 font-medium">Minimum Level:</span>
          <span class="ml-2 text-blue-900">{{ selectedItem.min_stock_level }} {{ selectedItem.unit }}</span>
        </div>
      </div>
      <div v-if="selectedItem.is_low_stock" class="mt-2">
        <p class="text-xs text-blue-600">
          💡 Suggested quantity: {{ suggestedQuantity }} {{ selectedItem.unit }}
          <button
            type="button"
            @click="formData.quantity_requested = suggestedQuantity"
            class="ml-2 text-blue-700 underline hover:text-blue-900"
          >
            Use this
          </button>
        </p>
      </div>
      <div v-if="selectedItem.current_stock === 0" class="mt-2 p-2 bg-red-100 border border-red-300 rounded">
        <p class="text-xs font-medium text-red-800">
          ⚠️ URGENT: Item is out of stock!
        </p>
      </div>
    </div>

    <BaseInput
      v-model.number="formData.quantity_requested"
      type="number"
      label="Quantity Requested"
      placeholder="Enter quantity"
      :error="errors.quantity_requested"
      :required="true"
      :min="1"
    />

    <BaseInput
      v-model="formData.requested_by"
      label="Requested By"
      placeholder="Enter name or department"
      :error="errors.requested_by"
      :required="true"
    />

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Notes (Optional)</label>
      <textarea
        v-model="formData.notes"
        rows="3"
        placeholder="Add any additional notes..."
        class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.notes }"
      ></textarea>
      <p v-if="errors.notes" class="mt-1 text-sm text-red-600">{{ errors.notes }}</p>
    </div>

    <div class="flex justify-end gap-3 pt-4 border-t">
      <BaseButton variant="secondary" @click="$emit('cancel')" :disabled="loading">
        Cancel
      </BaseButton>
      <BaseButton type="submit" variant="primary" :loading="loading" :disabled="loading">
        Submit Request
      </BaseButton>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import BaseInput from './BaseInput.vue'
import BaseSelect from './BaseSelect.vue'
import BaseButton from './BaseButton.vue'
import { useInventoryStore } from '../stores/inventory'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const store = useInventoryStore()

const formData = reactive({
  item_id: null,
  quantity_requested: 1,
  requested_by: '',
  notes: ''
})

const errors = reactive({
  item_id: null,
  quantity_requested: null,
  requested_by: null,
  notes: null
})

const selectedItem = computed(() => {
  if (!formData.item_id) return null
  return store.itemById(formData.item_id)
})

const suggestedQuantity = computed(() => {
  if (!selectedItem.value || !selectedItem.value.is_low_stock) return 0
  return Math.max(1, selectedItem.value.min_stock_level - selectedItem.value.current_stock)
})

// Sort items: low stock items first, then by name
const sortedItemOptions = computed(() => {
  const items = [...store.items]
  
  // Sort: low stock first, then by name
  items.sort((a, b) => {
    const aLow = a.is_low_stock ? 1 : 0
    const bLow = b.is_low_stock ? 1 : 0
    
    if (aLow !== bLow) return bLow - aLow // Low stock first
    return a.name.localeCompare(b.name) // Then alphabetical
  })
  
  return items.map(item => ({
    value: item.id,
    label: `${item.name} (${item.category_name})${item.is_low_stock ? ' ⚠️ Low Stock' : ''} - Stock: ${item.current_stock} ${item.unit}`
  }))
})

// Initialize form if item prop is provided
watch(() => props.item, (newItem) => {
  if (newItem) {
    formData.item_id = newItem.id
    if (newItem.is_low_stock) {
      formData.quantity_requested = suggestedQuantity.value || 1
    }
  }
}, { immediate: true })

// Watch item selection to update suggested quantity
watch(() => formData.item_id, (newItemId) => {
  if (newItemId && selectedItem.value?.is_low_stock) {
    formData.quantity_requested = suggestedQuantity.value || 1
  }
})

// Reset form when modal closes
watch(() => props.loading, (newVal) => {
  if (!newVal && formData.item_id) {
    // Form was submitted successfully, reset
    formData.item_id = null
    formData.quantity_requested = 1
    formData.requested_by = ''
    formData.notes = ''
    Object.keys(errors).forEach(key => {
      errors[key] = null
    })
  }
})

const validateForm = () => {
  let isValid = true

  // Clear previous errors
  Object.keys(errors).forEach(key => {
    errors[key] = null
  })

  // Validate item
  if (!formData.item_id) {
    errors.item_id = 'Item is required'
    isValid = false
  }

  // Validate quantity
  if (!formData.quantity_requested || formData.quantity_requested <= 0) {
    errors.quantity_requested = 'Quantity must be greater than 0'
    isValid = false
  }

  // Validate requested_by
  if (!formData.requested_by || formData.requested_by.trim() === '') {
    errors.requested_by = 'Requested by is required'
    isValid = false
  }

  return isValid
}

const handleSubmit = () => {
  if (validateForm()) {
    const payload = {
      item_id: formData.item_id,
      quantity_requested: formData.quantity_requested,
      requested_by: formData.requested_by.trim(),
      status: 'pending',
      notes: formData.notes || undefined
    }
    emit('submit', payload)
  }
}
</script>

