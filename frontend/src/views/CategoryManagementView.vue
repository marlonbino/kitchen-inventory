<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 dark:from-neutral-900 dark:via-neutral-900 dark:to-neutral-900 p-3 sm:p-4 md:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto w-full">
      <!-- Page Header -->
      <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Edit Categories</h1>
          <p class="text-gray-600 dark:text-gray-200 font-medium mt-1">Organize items your way</p>
        </div>
        <BaseButton variant="primary" @click="openAddModal">
          <svg class="w-5 h-5 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Add Category
        </BaseButton>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div v-for="n in 3" :key="n" class="bg-white dark:bg-neutral-800 rounded-lg shadow-md p-6 animate-pulse">
          <div class="h-4 bg-gray-200 dark:bg-neutral-700 rounded w-3/4 mb-3"></div>
          <div class="h-4 bg-gray-200 dark:bg-neutral-700 rounded w-1/2"></div>
        </div>
      </div>

      <!-- Error State -->
      <BaseCard v-else-if="error">
        <div class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-2 text-red-600">{{ error }}</p>
          <BaseButton variant="primary" @click="loadCategories" class="mt-4">
            Try Again
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Empty State -->
      <BaseCard v-else-if="categories.length === 0">
        <div class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          <p class="mt-2 text-gray-500">No categories found</p>
          <BaseButton variant="primary" @click="openAddModal" class="mt-4">
            Create First Category
          </BaseButton>
        </div>
      </BaseCard>

      <!-- Categories Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div
          v-for="category in categories"
          :key="category.id"
          class="group bg-gradient-to-br from-neutral-800 to-neutral-900 dark:from-neutral-800 dark:to-neutral-900 rounded-2xl p-6 border border-neutral-700 shadow-lg hover:shadow-2xl transition-all duration-300"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-3">
                <div class="p-2 bg-purple-500/20 rounded-lg">
                  <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                </div>
                <h3 class="text-lg font-bold text-white group-hover:text-gray-100 transition-colors">{{ category.name }}</h3>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-2xl font-extrabold text-blue-400">{{ category.item_count || 0 }}</span>
                <span class="text-sm text-gray-400">items</span>
              </div>
            </div>
            <div class="flex items-center gap-1 ml-2">
              <button
                @click="openEditModal(category)"
                class="text-blue-400 hover:text-blue-300 hover:bg-blue-500/10 rounded-lg p-2 transition-all duration-200"
                title="Edit"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                @click="openDeleteConfirm(category)"
                :disabled="category.item_count > 0"
                class="text-red-400 hover:text-red-300 hover:bg-red-500/10 disabled:text-gray-600 disabled:cursor-not-allowed disabled:hover:bg-transparent rounded-lg p-2 transition-all duration-200"
                title="Delete"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          
          <p v-if="category.description" class="text-sm text-gray-300 mb-3 line-clamp-2">
            {{ category.description }}
          </p>
          
          <div v-if="category.item_count > 0" class="mt-4 pt-3 border-t border-neutral-700">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <p class="text-xs text-gray-400">
                Cannot delete - in use by {{ category.item_count }} items
              </p>
            </div>
          </div>
          <div v-else class="mt-4 pt-3 border-t border-neutral-700">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p class="text-xs text-gray-400">
                No items - can be deleted
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Category Modal (Add/Edit) -->
      <BaseModal :show="showCategoryModal" @close="closeCategoryModal" :title="editingCategory ? 'Edit Category' : 'Add New Category'">
        <CategoryForm
          :category="editingCategory"
          :loading="categoryLoading"
          :submit-text="editingCategory ? 'Update Category' : 'Add Category'"
          @submit="handleCategorySubmit"
          @cancel="closeCategoryModal"
        />
      </BaseModal>

      <!-- Delete Confirmation Modal -->
      <ConfirmDialog
        :show="showDeleteConfirm"
        title="Delete Category"
        :message="getDeleteMessage()"
        confirm-text="Delete"
        cancel-text="Cancel"
        variant="danger"
        @confirm="handleDeleteCategory"
        @cancel="closeDeleteConfirm"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import CategoryForm from '../components/CategoryForm.vue'
import { getCategories, createCategory, updateCategory, deleteCategory } from '../services/api.js'

const toast = useToast()

// State
const loading = ref(false)
const error = ref(null)
const categories = ref([])
const categoryLoading = ref(false)

// Modal states
const showCategoryModal = ref(false)
const showDeleteConfirm = ref(false)
const editingCategory = ref(null)
const categoryToDelete = ref(null)

// Methods
const loadCategories = async () => {
  loading.value = true
  error.value = null
  try {
    categories.value = await getCategories()
  } catch (err) {
    error.value = err.userMessage || 'Failed to load categories'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const openAddModal = () => {
  editingCategory.value = null
  showCategoryModal.value = true
}

const openEditModal = (category) => {
  editingCategory.value = { ...category }
  showCategoryModal.value = true
}

const closeCategoryModal = () => {
  showCategoryModal.value = false
  editingCategory.value = null
  categoryLoading.value = false
}

const handleCategorySubmit = async (categoryData) => {
  categoryLoading.value = true
  try {
    if (editingCategory.value) {
      await updateCategory(editingCategory.value.id, categoryData)
      toast.success('Category updated successfully!')
    } else {
      await createCategory(categoryData)
      toast.success('Category added successfully!')
    }
    closeCategoryModal()
    await loadCategories() // Reload to refresh the list
  } catch (err) {
    toast.error(err.userMessage || 'Failed to save category')
  } finally {
    categoryLoading.value = false
  }
}

const openDeleteConfirm = (category) => {
  if (category.item_count > 0) {
    toast.warning('Cannot delete category with items. Please reassign items first.')
    return
  }
  categoryToDelete.value = category
  showDeleteConfirm.value = true
}

const closeDeleteConfirm = () => {
  showDeleteConfirm.value = false
  categoryToDelete.value = null
}

const handleDeleteCategory = async () => {
  if (!categoryToDelete.value) return
  try {
    await deleteCategory(categoryToDelete.value.id)
    toast.success('Category deleted successfully!')
    closeDeleteConfirm()
    await loadCategories()
  } catch (err) {
    toast.error(err.userMessage || 'Failed to delete category')
  }
}

const getDeleteMessage = () => {
  if (!categoryToDelete.value) return ''
  return `Are you sure you want to delete "${categoryToDelete.value.name}"?\n\nThis action cannot be undone.`
}

// Initial data load
onMounted(() => {
  loadCategories()
})
</script>

<script>
export default {
  name: 'CategoryManagementView'
}
</script>

