# Toast Notifications & Confirmation Dialogs Implementation Plan

## 🎯 Objective

Enhance UI feedback with comprehensive toast notifications and confirmation dialogs across all user actions in the Kitchen Inventory System. This plan provides implementation patterns, Vue component code snippets, and testing strategies.

## 📋 Current State Analysis

### ✅ Already Implemented
- **Toast Infrastructure**: `vue-toastification` configured in `main.js`
- **Base Components**: `ConfirmDialog.vue` exists with modal structure
- **Toast Configuration**: Position (top-right), timeout (3000ms), animations

### ❌ Missing Implementation
- Toast calls in view components
- Consistent success/error patterns
- Confirmation dialogs for destructive actions
- Visual testing strategies
- Component-level tests

## 🔧 Implementation Strategy

### Phase 1: Toast Notification Composable

Create a centralized toast composable for consistent usage across components.

**File**: `kitchen-inventory/frontend/src/composables/useToast.js`

```javascript
import { useToast as useVueToast } from 'vue-toastification'

export const useToast = () => {
  const toast = useVueToast()

  const showSuccess = (message, options = {}) => {
    return toast.success(message, {
      position: 'top-right',
      timeout: 3000,
      closeOnClick: true,
      pauseOnFocusLoss: true,
      pauseOnHover: true,
      draggable: true,
      draggablePercent: 0.6,
      hideProgressBar: false,
      ...options
    })
  }

  const showError = (message, options = {}) => {
    return toast.error(message, {
      position: 'top-right',
      timeout: 5000, // Longer timeout for errors
      closeOnClick: true,
      pauseOnFocusLoss: true,
      pauseOnHover: true,
      draggable: true,
      draggablePercent: 0.6,
      hideProgressBar: false,
      ...options
    })
  }

  const showInfo = (message, options = {}) => {
    return toast.info(message, {
      position: 'top-right',
      timeout: 3000,
      ...options
    })
  }

  const showWarning = (message, options = {}) => {
    return toast.warning(message, {
      position: 'top-right',
      timeout: 4000,
      ...options
    })
  }

  return {
    showSuccess,
    showError,
    showInfo,
    showWarning
  }
}
```

### Phase 2: Enhanced Confirmation Dialog

Enhance existing `ConfirmDialog.vue` with icons and better visual feedback.

**File**: `kitchen-inventory/frontend/src/components/ConfirmDialog.vue` (Enhanced)

```vue
<template>
  <BaseModal
    :show="show"
    :title="title"
    :closable="closable"
    @close="handleCancel"
  >
    <div class="py-4">
      <!-- Icon based on variant -->
      <div class="flex items-start gap-4">
        <div 
          class="flex-shrink-0 p-3 rounded-full"
          :class="iconClasses"
        >
          <component :is="iconComponent" class="w-6 h-6" />
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            {{ title }}
          </h3>
          <p class="text-gray-700 whitespace-pre-line">{{ message }}</p>
          
          <!-- Additional details for specific actions -->
          <div v-if="details" class="mt-3 p-3 bg-gray-50 rounded border border-gray-200">
            <p class="text-sm text-gray-600" v-html="details"></p>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <BaseButton
        variant="secondary"
        @click="handleCancel"
      >
        {{ cancelText }}
      </BaseButton>
      <BaseButton
        :variant="variant"
        @click="handleConfirm"
        :loading="loading"
      >
        {{ confirmText }}
      </BaseButton>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
import BaseModal from './BaseModal.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    required: true
  },
  details: {
    type: String,
    default: null
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  },
  closable: {
    type: Boolean,
    default: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['confirm', 'cancel', 'update:show'])

// Icon configuration based on variant
const iconComponent = computed(() => {
  const icons = {
    danger: 'ExclamationTriangle',
    warning: 'ExclamationCircle',
    primary: 'InformationCircle',
    secondary: 'QuestionMarkCircle'
  }
  return icons[props.variant] || 'QuestionMarkCircle'
})

const iconClasses = computed(() => {
  const classes = {
    danger: 'bg-red-100 text-red-600',
    warning: 'bg-yellow-100 text-yellow-600',
    primary: 'bg-blue-100 text-blue-600',
    secondary: 'bg-gray-100 text-gray-600'
  }
  return classes[props.variant] || 'bg-gray-100 text-gray-600'
})

const handleConfirm = () => {
  emit('confirm')
  emit('update:show', false)
}

const handleCancel = () => {
  emit('cancel')
  emit('update:show', false)
}
</script>

<!-- Icon components would be imported -->
<script>
// For this example, using simple SVGs
const ExclamationTriangle = {
  template: `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
  `
}

const ExclamationCircle = {
  template: `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
}

const InformationCircle = {
  template: `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
}

const QuestionMarkCircle = {
  template: `
    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
        d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
}
</script>
```

## 🎨 Integration Examples

### Example 1: Items View with Toasts & Confirmations

**File**: `kitchen-inventory/frontend/src/views/ItemListView-Enhanced.vue` (Snippet)

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from '../composables/useToast'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import ItemForm from '../components/ItemForm.vue'
import { useRouter } from 'vue-router'

const store = useInventoryStore()
const router = useRouter()
const toast = useToast()

// Modal states
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteConfirm = ref(false)
const showQuickStockModal = ref(false)

// Selected item for operations
const selectedItem = ref(null)

// Delete confirmation state
const deleteConfirmData = ref({
  title: 'Delete Item',
  message: '',
  variant: 'danger'
})

// Load items on mount
onMounted(async () => {
  try {
    await store.fetchItems()
  } catch (error) {
    toast.showError('Failed to load items. Please try again.')
  }
})

// Open Add Modal
const openAddModal = () => {
  showAddModal.value = true
}

// Handle Add Item Success
const handleAddSuccess = async (itemData) => {
  try {
    const newItem = await store.addItem(itemData)
    showAddModal.value = false
    toast.showSuccess(`Item "${newItem.name}" created successfully!`)
    await store.fetchItems() // Refresh list
  } catch (error) {
    toast.showError(error.userMessage || 'Failed to create item. Please try again.')
  }
}

// Open Edit Modal
const openEditModal = (item) => {
  selectedItem.value = item
  showEditModal.value = true
}

// Handle Edit Success
const handleEditSuccess = async (itemData) => {
  try {
    await store.updateItem(selectedItem.value.id, itemData)
    showEditModal.value = false
    toast.showSuccess(`Item "${itemData.name}" updated successfully!`)
    await store.fetchItems() // Refresh list
  } catch (error) {
    toast.showError(error.userMessage || 'Failed to update item. Please try again.')
  }
}

// Open Delete Confirmation
const openDeleteConfirm = (item) => {
  selectedItem.value = item
  deleteConfirmData.value = {
    title: 'Delete Item',
    message: `Are you sure you want to delete "${item.name}"?\n\nThis action cannot be undone.`,
    variant: 'danger'
  }
  showDeleteConfirm.value = true
}

// Handle Delete Confirmation
const handleDeleteConfirm = async () => {
  try {
    await store.deleteItem(selectedItem.value.id)
    toast.showSuccess(`Item "${selectedItem.value.name}" deleted successfully!`)
    await store.fetchItems() // Refresh list
  } catch (error) {
    toast.showError(error.userMessage || 'Failed to delete item. Please try again.')
  } finally {
    showDeleteConfirm.value = false
    selectedItem.value = null
  }
}

// Quick Stock Adjustment
const handleQuickStock = async (movementType, quantity) => {
  try {
    const movementData = {
      item_id: selectedItem.value.id,
      movement_type: movementType,
      quantity: quantity,
      reference: `QUICK-${movementType.toUpperCase()}-${Date.now()}`,
      notes: `Quick ${movementType} adjustment`
    }
    
    await store.addStockMovement(movementData)
    toast.showSuccess(`Stock ${movementType === 'receipt' ? 'added' : 'removed'} successfully!`)
    await store.fetchItems() // Refresh to show updated stock
  } catch (error) {
    toast.showError(error.userMessage || `Failed to adjust stock. ${error.message}`)
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
    <!-- ... existing template content ... -->

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      v-model:show="showDeleteConfirm"
      :title="deleteConfirmData.title"
      :message="deleteConfirmData.message"
      :variant="deleteConfirmData.variant"
      :closable="true"
      confirm-text="Delete"
      cancel-text="Cancel"
      @confirm="handleDeleteConfirm"
      @cancel="() => { selectedItem = null }"
    />

    <!-- Add Item Modal -->
    <ItemForm
      v-model:show="showAddModal"
      mode="create"
      @success="handleAddSuccess"
      @cancel="() => { showAddModal = false }"
    />

    <!-- Edit Item Modal -->
    <ItemForm
      v-if="selectedItem"
      v-model:show="showEditModal"
      mode="edit"
      :item="selectedItem"
      @success="handleEditSuccess"
      @cancel="() => { showEditModal = false; selectedItem = null }"
    />
  </div>
</template>
```

### Example 2: Stock Movements with Validation Toasts

**File**: Enhanced Stock Movement Handling

```vue
<script setup>
import { ref } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from '../composables/useToast'
import StockMovementForm from '../components/StockMovementForm.vue'

const store = useInventoryStore()
const toast = useToast()

const showAddModal = ref(false)
const showDeleteConfirm = ref(false)
const selectedMovement = ref(null)

const handleAddMovement = async (movementData) => {
  try {
    // Validate stock for issue/writeoff
    const item = store.itemById(movementData.item_id)
    
    if (['issue', 'writeoff'].includes(movementData.movement_type)) {
      const newStock = item.current_stock - movementData.quantity
      
      if (newStock < 0) {
        toast.showError(`Cannot ${movementData.movement_type}. Insufficient stock.`, {
          timeout: 6000
        })
        return
      }
      
      if (newStock < item.min_stock_level) {
        toast.showWarning(
          `Warning: This will bring stock below minimum level (${item.min_stock_level} ${item.unit}).`,
          { timeout: 5000 }
        )
      }
    }
    
    const newMovement = await store.addStockMovement(movementData)
    showAddModal.value = false
    
    toast.showSuccess(
      `${movementData.movement_type === 'receipt' ? 'Receipt' : movementData.movement_type === 'issue' ? 'Issue' : 'Write-off'} recorded successfully!`,
      {
        icon: true
      }
    )
    
    await store.fetchStockMovements()
    await store.fetchItems() // Update stock levels
  } catch (error) {
    toast.showError(error.userMessage || 'Failed to record movement. Please try again.', {
      timeout: 6000
    })
  }
}

const handleDeleteMovement = async () => {
  try {
    await store.deleteStockMovement(selectedMovement.value.id)
    toast.showSuccess('Movement deleted successfully!')
    await store.fetchStockMovements()
  } catch (error) {
    toast.showError(error.userMessage || 'Failed to delete movement.')
  } finally {
    showDeleteConfirm.value = false
    selectedMovement.value = null
  }
}
</script>
```

### Example 3: Requisitions with Status Change Feedback

**File**: Enhanced Requisition Handling

```vue
<script setup>
import { ref } from 'vue'
import { useInventoryStore } from '../stores/inventory'
import { useToast } from '../composables/useToast'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const store = useInventoryStore()
const toast = useToast()

const showConfirmDialog = ref(false)
const approveAction = ref(null) // 'approve' | 'reject'
const selectedRequisition = ref(null)

const confirmApprove = (req) => {
  selectedRequisition.value = req
  approveAction.value = 'approve'
  showConfirmDialog.value = true
}

const confirmReject = (req) => {
  selectedRequisition.value = req
  approveAction.value = 'reject'
  showConfirmDialog.value = true
}

const handleStatusChange = async () => {
  try {
    if (approveAction.value === 'approve') {
      await store.approveRequisition(selectedRequisition.value.id)
      toast.showSuccess(
        `Requisition for "${selectedRequisition.value.item.name}" approved!`,
        { icon: true }
      )
    } else {
      await store.rejectRequisition(selectedRequisition.value.id)
      toast.showSuccess(
        `Requisition for "${selectedRequisition.value.item.name}" rejected.`,
        { icon: true }
      )
    }
    
    await store.fetchRequisitions()
    await store.fetchItems()
  } catch (error) {
    toast.showError(error.userMessage || 'Failed to update requisition status.')
  } finally {
    showConfirmDialog.value = false
    selectedRequisition.value = null
    approveAction.value = null
  }
}

const getConfirmDialogProps = () => {
  if (!selectedRequisition.value) return {}
  
  return approveAction.value === 'approve' ? {
    title: 'Approve Requisition',
    message: `Approve request for ${selectedRequisition.value.quantity_requested} ${selectedRequisition.value.item.unit} of "${selectedRequisition.value.item.name}"?`,
    variant: 'primary',
    confirmText: 'Approve',
    details: `<div class="space-y-1">
      <p><strong>Requested by:</strong> ${selectedRequisition.value.requested_by}</p>
      <p><strong>Quantity:</strong> ${selectedRequisition.value.quantity_requested} ${selectedRequisition.value.item.unit}</p>
      <p><strong>Current stock:</strong> ${selectedRequisition.value.item.current_stock} ${selectedRequisition.value.item.unit}</p>
    </div>`
  } : {
    title: 'Reject Requisition',
    message: `Reject request for ${selectedRequisition.value.quantity_requested} ${selectedRequisition.value.item.unit} of "${selectedRequisition.value.item.name}"?`,
    variant: 'danger',
    confirmText: 'Reject',
    details: `<div class="space-y-1">
      <p><strong>Requested by:</strong> ${selectedRequisition.value.requested_by}</p>
      <p><strong>Note:</strong> The requester will be notified of this rejection.</p>
    </div>`
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
    <!-- ... existing template ... -->

    <!-- Status Change Confirmation -->
    <ConfirmDialog
      v-model:show="showConfirmDialog"
      v-bind="getConfirmDialogProps()"
      @confirm="handleStatusChange"
      @cancel="() => { selectedRequisition = null; approveAction = null }"
    />
  </div>
</template>
```

## 🧪 Testing Strategy

### Testing Approach

#### 1. Component-level tests

Add tests for dialog triggers and toast calls with `@testing-library/vue`.

**File**: `kitchen-inventory/frontend/src/components/__tests__/ConfirmDialog.spec.js`

```javascript
import { mount } from '@vue/test-utils'
import { vi } from 'vitest'
import ConfirmDialog from '../ConfirmDialog.vue'

describe('ConfirmDialog', () => {
  it('renders with correct props', () => {
    const wrapper = mount(ConfirmDialog, {
      props: {
        show: true,
        title: 'Delete Item',
        message: 'Are you sure?',
        variant: 'danger'
      }
    })
    
    expect(wrapper.find('[role="dialog"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('Delete Item')
    expect(wrapper.text()).toContain('Are you sure?')
  })
  
  it('emits confirm when confirm button clicked', async () => {
    const wrapper = mount(ConfirmDialog, {
      props: {
        show: true,
        message: 'Test message'
      }
    })
    
    await wrapper.find('button:contains("Confirm")').trigger('click')
    expect(wrapper.emitted('confirm')).toBeTruthy()
  })
  
  it('emits cancel when cancel button clicked', async () => {
    const wrapper = mount(ConfirmDialog, {
      props: {
        show: true,
        message: 'Test message'
      }
    })
    
    await wrapper.find('button:contains("Cancel")').trigger('click')
    expect(wrapper.emitted('cancel')).toBeTruthy()
  })
  
  it('shows loading state on confirm button', () => {
    const wrapper = mount(ConfirmDialog, {
      props: {
        show: true,
        message: 'Test message',
        loading: true
      }
    })
    
    const confirmBtn = wrapper.find('button:contains("Confirm")')
    expect(confirmBtn.attributes('disabled')).toBeDefined()
  })
})
```

**File**: `kitchen-inventory/frontend/src/composables/__tests__/useToast.spec.js`

```javascript
import { describe, it, expect, vi } from 'vitest'
import { useToast } from '../useToast'

// Mock vue-toastification
const mockToast = {
  success: vi.fn(),
  error: vi.fn(),
  info: vi.fn(),
  warning: vi.fn()
}

vi.mock('vue-toastification', () => ({
  useToast: () => mockToast
}))

describe('useToast', () => {
  it('shows success toast with default options', () => {
    const { showSuccess } = useToast()
    showSuccess('Success message')
    
    expect(mockToast.success).toHaveBeenCalledWith(
      'Success message',
      expect.objectContaining({
        position: 'top-right',
        timeout: 3000
      })
    )
  })
  
  it('shows error toast with longer timeout', () => {
    const { showError } = useToast()
    showError('Error message')
    
    expect(mockToast.error).toHaveBeenCalledWith(
      'Error message',
      expect.objectContaining({
        timeout: 5000
      })
    )
  })
})
```

#### 2. Storybook

Add stories for dialog and toast states.

**File**: `kitchen-inventory/frontend/src/stories/ConfirmDialog.stories.js`

```javascript
import ConfirmDialog from '../components/ConfirmDialog.vue'

export default {
  title: 'Components/ConfirmDialog',
  component: ConfirmDialog,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'danger', 'warning']
    }
  }
}

export const Default = {
  args: {
    show: true,
    title: 'Confirm Action',
    message: 'Are you sure you want to proceed?',
    variant: 'primary'
  }
}

export const Danger = {
  args: {
    show: true,
    title: 'Delete Item',
    message: 'Are you sure you want to delete this item?\n\nThis action cannot be undone.',
    variant: 'danger',
    confirmText: 'Delete'
  }
}

export const WithDetails = {
  args: {
    show: true,
    title: 'Approve Requisition',
    message: 'Approve this requisition request?',
    variant: 'primary',
    details: `
      <div>
        <p><strong>Item:</strong> Milk</p>
        <p><strong>Quantity:</strong> 50 bottles</p>
        <p><strong>Requested by:</strong> Chef John</p>
      </div>
    `
  }
}

export const Loading = {
  args: {
    show: true,
    title: 'Processing',
    message: 'Please wait while we process your request.',
    variant: 'primary',
    loading: true,
    confirmText: 'Processing...'
  }
}
```

**File**: `kitchen-inventory/frontend/src/stories/Toast.stories.js`

```javascript
import { useToast } from '../composables/useToast'

export default {
  title: 'Feedback/ToastNotifications',
  parameters: {
    docs: {
      description: {
        component: 'Toast notification examples showing different types and states.'
      }
    }
  }
}

export const SuccessToast = () => ({
  setup() {
    const toast = useToast()
    
    return {
      showToast: () => toast.showSuccess('Item created successfully!')
    }
  },
  template: `
    <div class="p-8">
      <button 
        @click="showToast" 
        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Show Success Toast
      </button>
    </div>
  `
})

export const ErrorToast = () => ({
  setup() {
    const toast = useToast()
    
    return {
      showToast: () => toast.showError('Failed to create item. Please try again.')
    }
  },
  template: `
    <div class="p-8">
      <button 
        @click="showToast" 
        class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Show Error Toast
      </button>
    </div>
  `
})

export const WarningToast = () => ({
  setup() {
    const toast = useToast()
    
    return {
      showToast: () => toast.showWarning('Stock will go below minimum level!')
    }
  },
  template: `
    <div class="p-8">
      <button 
        @click="showToast" 
        class="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
      >
        Show Warning Toast
      </button>
    </div>
  `
})

export const InfoToast = () => ({
  setup() {
    const toast = useToast()
    
    return {
      showToast: () => toast.showInfo('Auto-saving changes...')
    }
  },
  template: `
    <div class="p-8">
      <button 
        @click="showToast" 
        class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Show Info Toast
      </button>
    </div>
  `
})
```

#### 3. Cypress E2E

Verify toasts and dialogs end-to-end.

**File**: `kitchen-inventory/frontend/cypress/e2e/toasts-and-dialogs.cy.js`

```javascript
describe('Toast Notifications & Dialogs E2E', () => {
  beforeEach(() => {
    cy.visit('/items')
    cy.waitForPageLoad()
  })

  describe('Toast Notifications', () => {
    it('shows success toast when creating item', () => {
      cy.contains('button', 'Add New Item').click()
      
      cy.fillInput('Name', 'Toast Test Item')
      cy.get('label').contains('Category').parent().find('select').select('Produce')
      cy.get('label').contains('Unit').parent().find('select').select('kg')
      cy.fillInput('Minimum Stock Level', '20')
      cy.fillInput('Current Stock', '50')
      
      cy.contains('button', 'Create').click()
      
      cy.get('.Vue-Toastification__toast').should('be.visible')
      cy.get('.Vue-Toastification__toast').should('contain', 'success')
      cy.get('.Vue-Toastification__toast').should('contain', 'created successfully')
    })

    it('shows error toast when validation fails', () => {
      cy.contains('button', 'Add New Item').click()
      cy.contains('button', 'Create').click()
      
      cy.get('.Vue-Toastification__toast').should('be.visible')
      cy.get('.Vue-Toastification__toast').should('have.class', 'Vue-Toastification__toast--error')
    })

    it('shows warning toast when stock goes below minimum', () => {
      cy.visit('/movements')
      cy.waitForPageLoad()
      
      cy.contains('button', 'Record Movement').click()
      
      cy.get('label').contains('Item').parent().find('select').select('Tomatoes')
      cy.get('label').contains('Movement Type').parent().find('select').select('issue')
      cy.fillInput('Quantity', '10')
      
      cy.get('[class*="warning"]').should('exist')
    })
  })

  describe('Confirmation Dialogs', () => {
    it('shows confirmation dialog when deleting item', () => {
      cy.wait(2000)
      
      cy.get('button[aria-label*="Delete"]').then($buttons => {
        if ($buttons.length > 0) {
          cy.wrap($buttons.first()).click({ force: true })
          
          cy.get('[role="dialog"]').should('be.visible')
          cy.get('[role="dialog"]').should('contain', 'Delete')
          cy.get('[role="dialog"]').should('contain', 'Are you sure')
          
          cy.contains('button', 'Cancel').click()
        }
      })
    })

    it('executes delete when confirmed', () => {
      cy.wait(2000)
      
      cy.get('button[aria-label*="Delete"]').then($buttons => {
        if ($buttons.length > 1) {
          const itemName = $buttons.eq(1).closest('div, tr').find('text, span').first().text()
          
          cy.wrap($buttons.eq(1)).click({ force: true })
          
          cy.wait(500)
          cy.contains('button', 'Delete').click()
          
          cy.waitForToast('success')
          cy.wait(1000)
          cy.get('body').should('not.contain', itemName)
        }
      })
    })

    it('cancels delete when cancel clicked', () => {
      cy.wait(2000)
      
      cy.get('button[aria-label*="Delete"]').then($buttons => {
        if ($buttons.length > 0) {
          const itemName = $buttons.first().closest('div, tr').find('text, span').first().text()
          
          cy.wrap($buttons.first()).click({ force: true })
          
          cy.wait(500)
          cy.contains('button', 'Cancel').click()
          
          cy.contains(itemName).should('exist')
        }
      })
    })
  })

  describe('Requisition Workflows', () => {
    it('shows confirmation and success toast when approving', () => {
      cy.visit('/requisitions')
      cy.waitForPageLoad()
      
      cy.contains('button', 'Pending').click()
      cy.wait(1000)
      
      cy.contains('button', 'Approve').then($buttons => {
        if ($buttons.length > 0) {
          cy.wrap($buttons.first()).click()
          
          cy.get('[role="dialog"]').should('be.visible')
          cy.contains('button', 'Approve').click()
          
          cy.waitForToast('success')
        }
      })
    })

    it('shows confirmation and success toast when rejecting', () => {
      cy.visit('/requisitions')
      cy.waitForPageLoad()
      
      cy.contains('button', 'Pending').click()
      cy.wait(1000)
      
      cy.contains('button', 'Reject').then($buttons => {
        if ($buttons.length > 0) {
          cy.wrap($buttons.first()).click()
          
          cy.get('[role="dialog"]').should('be.visible')
          cy.contains('button', 'Reject').click()
          
          cy.waitForToast('success')
        }
      })
    })
  })
})
```

## 📊 Implementation Checklist

### Phase 1: Foundation
- [ ] Create `useToast.js` composable
- [ ] Enhance `ConfirmDialog.vue` with icons and details
- [ ] Add BaseButton loading prop support
- [ ] Update main.js toast configuration

### Phase 2: Integration
- [ ] Integrate toasts in ItemListView
- [ ] Integrate toasts in StockMovementHistoryView
- [ ] Integrate toasts in RequisitionManagerView
- [ ] Add confirmations for all delete actions
- [ ] Add confirmations for approve/reject actions
- [ ] Add warnings for stock level issues

### Phase 3: Testing
- [ ] Component tests for ConfirmDialog
- [ ] Component tests for useToast
- [ ] Storybook stories for all dialog variants
- [ ] Storybook stories for all toast types
- [ ] Cypress E2E tests for toast flows
- [ ] Cypress E2E tests for dialog flows

### Phase 4: Documentation
- [ ] Usage guidelines for toasts
- [ ] Usage guidelines for confirmations
- [ ] Best practices
- [ ] Common patterns

## 🎨 Visual Verification Scenarios

### Scenario 1: Item Creation Success
- Action: Create a new item
- Toast: success, green icon, short timeout
- Visual: slide-in, progress bar, close on click

### Scenario 2: Delete Item Warning
- Action: Delete an item
- Dialog: red icon, clear message, details
- Toast: success after confirm
- Visual: modal overlay, focus trap, ESC closes

### Scenario 3: Stock Movement Validation
- Action: Issue below minimum
- Warning: yellow toast before submit
- Success: green after submit
- Visual: both visible and sequenced

### Scenario 4: Network Error
- Action: Delete with offline
- Toast: error, longer timeout, clear message
- Visual: red icon, retry option

### Scenario 5: Requisition Approve with Context
- Action: Approve
- Dialog: details, blue icon, primary variant
- Toast: success with item name
- Visual: details shown, accurate icons

## 🚀 Quick Start

1. Install dependencies:
```bash
npm install @vue/test-utils vitest @testing-library/jest-dom
npm install -D @storybook/vue3 @storybook/addon-docs
```

2. Create composable: `src/composables/useToast.js`

3. Update ConfirmDialog: `src/components/ConfirmDialog.vue`

4. Integrate in views

5. Add tests

6. Add Storybook stories

This provides a complete, testable plan for toasts and confirmations with example code and tests.

