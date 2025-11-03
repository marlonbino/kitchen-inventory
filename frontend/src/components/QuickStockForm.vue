<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div class="mb-4">
      <p class="text-sm text-gray-600">
        Item: <span class="font-semibold text-gray-900">{{ itemName }}</span>
      </p>
      <p class="text-xs text-gray-500 mt-1">
        Current Stock: <span class="font-medium">{{ currentStock }}</span> {{ unit }}
      </p>
    </div>

    <BaseInput
      v-model.number="formData.quantity"
      type="number"
      label="Quantity"
      :placeholder="`Enter quantity in ${unit}`"
      :error="errors.quantity"
      :required="true"
      :min="1"
    />

    <BaseInput
      v-if="showReference"
      v-model="formData.reference"
      label="Reference (Optional)"
      placeholder="e.g., PO-12345, Invoice #456"
      :error="errors.reference"
    />

    <BaseInput
      v-if="showNotes"
      v-model="formData.notes"
      type="text"
      label="Notes (Optional)"
      placeholder="Add any additional notes"
      :error="errors.notes"
    />

    <div
      v-if="movementType === 'usage'"
      class="p-3 bg-orange-50 border border-orange-200 rounded-md"
    >
      <div class="flex items-start">
        <svg class="w-5 h-5 mt-0.5 mr-2 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <p class="text-sm font-medium text-orange-800">
            Stock will decrease after usage:
          </p>
          <p class="text-sm text-orange-700 mt-1">
            Current: {{ currentStock }} {{ unit }} → After: <span class="font-semibold">{{ projectedStock }}</span> {{ unit }}
          </p>
        </div>
      </div>
    </div>
    
    <div
      v-if="movementType === 'receipt'"
      class="p-3 bg-blue-50 border border-blue-200 rounded-md"
    >
      <div class="flex items-start">
        <svg class="w-5 h-5 mt-0.5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <p class="text-sm font-medium text-blue-800">
            Stock will increase after delivery:
          </p>
          <p class="text-sm text-blue-700 mt-1">
            Current: {{ currentStock }} {{ unit }} → After: <span class="font-semibold">{{ projectedStock }}</span> {{ unit }}
          </p>
        </div>
      </div>
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
        :variant="movementType === 'usage' ? 'secondary' : 'primary'"
        :loading="loading"
        :disabled="loading"
      >
        {{ submitText }}
      </BaseButton>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import BaseInput from './BaseInput.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  itemId: {
    type: Number,
    required: true
  },
  itemName: {
    type: String,
    required: true
  },
  currentStock: {
    type: Number,
    required: true
  },
  unit: {
    type: String,
    default: 'units'
  },
  movementType: {
    type: String,
    required: true,
    validator: (value) => ['receipt', 'usage'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  showReference: {
    type: Boolean,
    default: true
  },
  showNotes: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = reactive({
  quantity: 1,
  reference: '',
  notes: ''
})

const errors = reactive({
  quantity: null,
  reference: null,
  notes: null
})

const submitText = computed(() => {
  if (props.movementType === 'receipt') return 'Receive Delivery'
  if (props.movementType === 'usage') return 'Track Usage'
  return 'Submit'
})

const projectedStock = computed(() => {
  if (props.movementType === 'receipt') {
    return props.currentStock + (formData.quantity || 0)
  }
  if (props.movementType === 'usage') {
    return Math.max(0, props.currentStock - (formData.quantity || 0))
  }
  return props.currentStock
})

// Reset form when component is shown
watch(() => props.itemId, () => {
  formData.quantity = 1
  formData.reference = ''
  formData.notes = ''
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

  // Validate quantity
  if (!formData.quantity || formData.quantity <= 0) {
    errors.quantity = 'Quantity must be greater than 0'
    isValid = false
  }

  return isValid
}

const handleSubmit = () => {
  if (validateForm()) {
    const payload = {
      item_id: props.itemId,
      movement_type: props.movementType,
      quantity: formData.quantity,
      reference: formData.reference || undefined,
      notes: formData.notes || undefined
    }
    emit('submit', payload)
  }
}
</script>

