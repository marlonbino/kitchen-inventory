<template>
  <div class="mb-4">
    <label
      v-if="label"
      :for="selectId"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500" aria-label="required">*</span>
    </label>
    <select
      :id="selectId"
      :value="modelValue"
      :disabled="disabled"
      :required="required"
      :class="selectClasses"
      :aria-invalid="!!error"
      :aria-describedby="error ? `${selectId}-error` : null"
      @change="handleChange"
      @blur="handleBlur"
    >
      <option v-if="placeholder" value="" disabled>
        {{ placeholder }}
      </option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
    <p
      v-if="error"
      :id="`${selectId}-error`"
      class="mt-1 text-sm text-red-600"
      role="alert"
    >
      {{ error }}
    </p>
    <p
      v-else-if="helpText"
      class="mt-1 text-sm text-gray-500"
    >
      {{ helpText }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: null
  },
  label: {
    type: String,
    default: null
  },
  options: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(option => 
        typeof option === 'object' && 
        option.hasOwnProperty('value') && 
        option.hasOwnProperty('label')
      )
    }
  },
  placeholder: {
    type: String,
    default: 'Select an option...'
  },
  error: {
    type: String,
    default: null
  },
  helpText: {
    type: String,
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'blur'])

// Generate unique ID for select
const selectId = computed(() => `select-${Math.random().toString(36).substr(2, 9)}`)

const selectClasses = computed(() => {
  const baseClasses = 'block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-0 transition-colors duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed bg-white'
  
  if (props.error) {
    return `${baseClasses} border-red-300 focus:border-red-500 focus:ring-red-500`
  }
  
  return `${baseClasses} border-gray-300 focus:border-blue-500 focus:ring-blue-500`
})

const handleChange = (event) => {
  const value = event.target.value
  // Convert to number if the original value was a number
  const numericValue = props.options.find(opt => String(opt.value) === value)?.value
  emit('update:modelValue', typeof numericValue === 'number' ? numericValue : value)
}

const handleBlur = (event) => {
  emit('blur', event)
}
</script>

