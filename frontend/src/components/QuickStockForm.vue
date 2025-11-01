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
      v-if="movementType === 'issue' && currentStock > 0"
      class="p-3 bg-yellow-50 border border-yellow-200 rounded-md"
    >
      <p class="text-sm text-yellow-800">
        After this movement, stock will be: <span class="font-semibold">{{ projectedStock }}</span> {{ unit }}
      </p>
    </div>

    <div
      v-if="movementType === 'issue' && formData.quantity > currentStock"
      class="p-3 bg-red-50 border border-red-200 rounded-md"
    >
      <p class="text-sm text-red-800">
        ⚠️ Cannot issue {{ formData.quantity }} {{ unit }}. Current stock is only {{ currentStock }} {{ unit }}.
      </p>
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
        :variant="movementType === 'issue' ? 'danger' : 'primary'"
        :loading="loading"
        :disabled="loading || (movementType === 'issue' && formData.quantity > currentStock)"
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
    validator: (value) => ['receipt', 'issue'].includes(value)
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
  if (props.movementType === 'receipt') return 'Add Receipt'
  if (props.movementType === 'issue') return 'Issue Stock'
  return 'Submit'
})

const projectedStock = computed(() => {
  if (props.movementType === 'receipt') {
    return props.currentStock + (formData.quantity || 0)
  } else {
    return Math.max(0, props.currentStock - (formData.quantity || 0))
  }
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
  } else if (props.movementType === 'issue' && formData.quantity > props.currentStock) {
    errors.quantity = `Cannot issue more than available stock (${props.currentStock} ${props.unit})`
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

