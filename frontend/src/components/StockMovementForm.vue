<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <BaseSelect
      v-model="formData.item_id"
      label="Item"
      :options="itemOptions"
      :error="errors.item_id"
      :required="true"
      placeholder="Search and select an item..."
    />

    <BaseSelect
      v-model="formData.movement_type"
      label="Movement Type"
      :options="movementTypeOptions"
      :error="errors.movement_type"
      :required="true"
    />

    <BaseInput
      v-model.number="formData.quantity"
      type="number"
      label="Quantity"
      placeholder="Enter quantity"
      :error="errors.quantity"
      :required="true"
      :min="1"
    />

    <BaseInput
      v-model="formData.reference"
      label="Reference (Optional)"
      placeholder="e.g., PO-12345, Invoice #456"
      :error="errors.reference"
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

    <!-- Stock Warning for Issue/Writeoff -->
    <div
      v-if="selectedItem && ['issue', 'writeoff'].includes(formData.movement_type) && formData.quantity > 0"
      class="p-3 rounded-md"
      :class="
        projectedStock < selectedItem.min_stock_level
          ? 'bg-yellow-50 border border-yellow-200'
          : 'bg-blue-50 border border-blue-200'
      "
    >
      <div class="flex items-start">
        <svg
          class="w-5 h-5 mt-0.5 mr-2"
          :class="
            projectedStock < selectedItem.min_stock_level
              ? 'text-yellow-600'
              : 'text-blue-600'
          "
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <div class="flex-1">
          <p
            class="text-sm font-medium"
            :class="
              projectedStock < selectedItem.min_stock_level
                ? 'text-yellow-800'
                : 'text-blue-800'
            "
          >
            <span v-if="projectedStock < selectedItem.min_stock_level">
              ⚠️ Warning: This will result in low stock!
            </span>
            <span v-else>Stock after movement:</span>
          </p>
          <p
            class="text-sm mt-1"
            :class="
              projectedStock < selectedItem.min_stock_level
                ? 'text-yellow-700'
                : 'text-blue-700'
            "
          >
            Current: {{ selectedItem.current_stock }} {{ selectedItem.unit }} → After:
            {{ projectedStock }} {{ selectedItem.unit }}
          </p>
          <p
            v-if="projectedStock < selectedItem.min_stock_level"
            class="text-xs mt-1 text-yellow-600"
          >
            Minimum stock level is {{ selectedItem.min_stock_level }} {{ selectedItem.unit }}
          </p>
        </div>
      </div>
    </div>

    <!-- Stock Validation Error -->
    <div
      v-if="selectedItem && ['issue', 'writeoff'].includes(formData.movement_type) && formData.quantity > selectedItem.current_stock"
      class="p-3 bg-red-50 border border-red-200 rounded-md"
    >
      <p class="text-sm text-red-800">
        ⚠️ Cannot {{ formData.movement_type }} {{ formData.quantity }} {{ selectedItem.unit }}.
        Current stock is only {{ selectedItem.current_stock }} {{ selectedItem.unit }}.
      </p>
    </div>

    <div class="flex justify-end gap-3 pt-4 border-t">
      <BaseButton variant="secondary" @click="$emit('cancel')" :disabled="loading">
        Cancel
      </BaseButton>
      <BaseButton
        type="submit"
        variant="primary"
        :loading="loading"
        :disabled="loading || hasInvalidStock"
      >
        Record Movement
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
  }
})

const emit = defineEmits(['submit', 'cancel'])

const store = useInventoryStore()

const movementTypeOptions = [
  { value: 'receipt', label: 'Receipt' },
  { value: 'issue', label: 'Issue' },
  { value: 'writeoff', label: 'Write-off' }
]

const itemOptions = computed(() => {
  return store.items.map(item => ({
    value: item.id,
    label: `${item.name} (${item.category}) - Stock: ${item.current_stock} ${item.unit}`
  }))
})

const formData = reactive({
  item_id: null,
  movement_type: '',
  quantity: 1,
  reference: '',
  notes: ''
})

const errors = reactive({
  item_id: null,
  movement_type: null,
  quantity: null,
  reference: null,
  notes: null
})

const selectedItem = computed(() => {
  if (!formData.item_id) return null
  return store.itemById(formData.item_id)
})

const projectedStock = computed(() => {
  if (!selectedItem.value || !formData.quantity) return 0
  
  if (formData.movement_type === 'receipt') {
    return selectedItem.value.current_stock + formData.quantity
  } else if (['issue', 'writeoff'].includes(formData.movement_type)) {
    return Math.max(0, selectedItem.value.current_stock - formData.quantity)
  }
  return selectedItem.value.current_stock
})

const hasInvalidStock = computed(() => {
  if (!selectedItem.value || formData.movement_type === 'receipt') return false
  return formData.quantity > selectedItem.value.current_stock
})

// Reset form when modal closes
watch(() => props.loading, (newVal) => {
  if (!newVal && formData.item_id) {
    // Form was submitted successfully, reset
    formData.item_id = null
    formData.movement_type = ''
    formData.quantity = 1
    formData.reference = ''
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

  // Validate movement type
  if (!formData.movement_type) {
    errors.movement_type = 'Movement type is required'
    isValid = false
  }

  // Validate quantity
  if (!formData.quantity || formData.quantity <= 0) {
    errors.quantity = 'Quantity must be greater than 0'
    isValid = false
  } else if (
    selectedItem.value &&
    ['issue', 'writeoff'].includes(formData.movement_type) &&
    formData.quantity > selectedItem.value.current_stock
  ) {
    errors.quantity = `Cannot ${formData.movement_type} more than available stock`
    isValid = false
  }

  return isValid
}

const handleSubmit = () => {
  if (validateForm()) {
    const payload = {
      item_id: formData.item_id,
      movement_type: formData.movement_type,
      quantity: formData.quantity,
      reference: formData.reference || undefined,
      notes: formData.notes || undefined
    }
    emit('submit', payload)
  }
}
</script>

