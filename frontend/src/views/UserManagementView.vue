<template>
  <div class="p-4 sm:p-6 lg:p-8 w-full max-w-full overflow-x-hidden">
    <div class="max-w-7xl mx-auto space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">User Management</h1>
          <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
            Create and manage system users
          </p>
        </div>
        <BaseButton
          @click="showCreateModal = true"
          variant="primary"
          class="flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Create User
        </BaseButton>
      </div>

      <!-- Users Table -->
      <BaseCard>
        <template #title>
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-blue-500 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            System Users
          </div>
        </template>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 dark:border-blue-400"></div>
        </div>

        <!-- Users List -->
        <div v-else-if="users.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
            <thead class="bg-gray-50/50 dark:bg-neutral-700/50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  User
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Email
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Role
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Joined
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-neutral-800 divide-y divide-gray-200 dark:divide-neutral-700">
              <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-neutral-700/50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div :class="[
                      'w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm',
                      getRoleGradient(user.role)
                    ]">
                      {{ user.username.charAt(0).toUpperCase() }}
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900 dark:text-white">
                        {{ user.username }}
                      </div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">
                        ID: {{ user.id }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900 dark:text-white">
                    {{ user.email || 'N/A' }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide',
                    getRoleBadgeClass(user.role)
                  ]">
                    {{ getRoleLabel(user.role) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(user.date_joined) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                    user.is_active 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' 
                      : 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
                  ]">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    v-if="currentUserId !== user.id"
                    @click="confirmDelete(user)"
                    class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300 transition-colors"
                    title="Delete User"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                  <span v-else class="text-gray-400 dark:text-gray-600 text-xs">
                    You
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">No users</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Get started by creating a new user.</p>
        </div>
      </BaseCard>

      <!-- Create User Modal -->
      <BaseModal :show="showCreateModal" title="Create New User" @close="closeCreateModal">
        <form @submit.prevent="handleCreateUser" class="space-y-4">
          <div v-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>

          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Username <span class="text-red-500">*</span>
            </label>
            <input
              id="username"
              v-model="newUser.username"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white"
              placeholder="Enter username"
            />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="newUser.email"
              type="email"
              class="w-full px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white"
              placeholder="user@example.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Password <span class="text-red-500">*</span>
            </label>
            <input
              id="password"
              v-model="newUser.password"
              type="password"
              required
              minlength="8"
              class="w-full px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white"
              placeholder="Minimum 8 characters"
            />
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Password must be at least 8 characters long</p>
          </div>

          <div>
            <label for="role" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Role <span class="text-red-500">*</span>
            </label>
            <select
              id="role"
              v-model="newUser.role"
              required
              class="w-full px-4 py-2 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white"
            >
              <option value="kitchen_staff">Kitchen Staff</option>
              <option value="manager">Manager</option>
              <option value="admin">Administrator</option>
            </select>
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Assign the appropriate role for this user</p>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <BaseButton
              type="button"
              variant="secondary"
              @click="closeCreateModal"
            >
              Cancel
            </BaseButton>
            <BaseButton
              type="submit"
              variant="primary"
              :disabled="createLoading"
            >
              <span v-if="createLoading">Creating...</span>
              <span v-else>Create User</span>
            </BaseButton>
          </div>
        </form>
      </BaseModal>

      <!-- Delete Confirmation Modal -->
      <BaseModal :show="showDeleteModal" title="Confirm Delete" @close="showDeleteModal = false">
        <div class="space-y-4">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Are you sure you want to delete the user <strong class="text-gray-900 dark:text-white">{{ userToDelete?.username }}</strong>?
          </p>
          <p class="text-sm text-red-600 dark:text-red-400">
            ⚠️ This action cannot be undone. All data associated with this user will be permanently removed.
          </p>
          <div class="flex justify-end gap-3 pt-4">
            <BaseButton
              type="button"
              variant="secondary"
              @click="showDeleteModal = false"
            >
              Cancel
            </BaseButton>
            <BaseButton
              type="button"
              variant="danger"
              @click="handleDeleteUser"
              :disabled="deleteLoading"
            >
              <span v-if="deleteLoading">Deleting...</span>
              <span v-else>Delete User</span>
            </BaseButton>
          </div>
        </div>
      </BaseModal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import BaseCard from '../components/BaseCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseModal from '../components/BaseModal.vue'
import { getUsers, createUser, deleteUser, getUserInfo } from '../services/api.js'

const router = useRouter()
const toast = useToast()

const users = ref([])
const loading = ref(false)
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const createLoading = ref(false)
const deleteLoading = ref(false)
const error = ref('')
const userToDelete = ref(null)
const currentUserId = ref(null)

const newUser = ref({
  username: '',
  email: '',
  password: '',
  role: 'kitchen_staff'
})

const loadUsers = async () => {
  loading.value = true
  try {
    const response = await getUsers()
    users.value = response.users || []
  } catch (err) {
    console.error('Failed to load users:', err)
    toast.error('Failed to load users')
    
    // If unauthorized, redirect to login or dashboard
    if (err.response?.status === 403) {
      toast.error('You do not have permission to access this page')
      router.push('/')
    }
  } finally {
    loading.value = false
  }
}

const handleCreateUser = async () => {
  error.value = ''
  createLoading.value = true

  try {
    await createUser(newUser.value)
    toast.success('User created successfully')
    closeCreateModal()
    await loadUsers()
  } catch (err) {
    console.error('Failed to create user:', err)
    error.value = err.response?.data?.error || 'Failed to create user'
  } finally {
    createLoading.value = false
  }
}

const confirmDelete = (user) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const handleDeleteUser = async () => {
  if (!userToDelete.value) return

  deleteLoading.value = true
  try {
    await deleteUser(userToDelete.value.id)
    toast.success(`User "${userToDelete.value.username}" deleted successfully`)
    showDeleteModal.value = false
    userToDelete.value = null
    await loadUsers()
  } catch (err) {
    console.error('Failed to delete user:', err)
    toast.error(err.response?.data?.error || 'Failed to delete user')
  } finally {
    deleteLoading.value = false
  }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  error.value = ''
  newUser.value = {
    username: '',
    email: '',
    password: '',
    role: 'kitchen_staff'
  }
}

const getRoleLabel = (role) => {
  const labels = {
    'admin': 'Admin',
    'manager': 'Manager',
    'kitchen_staff': 'Staff'
  }
  return labels[role] || role
}

const getRoleBadgeClass = (role) => {
  if (role === 'admin') {
    return 'bg-gradient-to-r from-purple-500 to-purple-600 text-white shadow-md shadow-purple-500/30'
  } else if (role === 'manager') {
    return 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md shadow-blue-500/30'
  } else {
    return 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-md shadow-green-500/30'
  }
}

const getRoleGradient = (role) => {
  if (role === 'admin') {
    return 'bg-gradient-to-br from-purple-500 to-purple-700'
  } else if (role === 'manager') {
    return 'bg-gradient-to-br from-blue-500 to-blue-700'
  } else {
    return 'bg-gradient-to-br from-green-500 to-green-700'
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

onMounted(async () => {
  // Get current user info
  try {
    const userInfo = await getUserInfo()
    currentUserId.value = userInfo.id
  } catch (err) {
    console.error('Failed to get user info:', err)
  }
  
  await loadUsers()
})
</script>

<style scoped>
/* Remove all table borders */
table {
  border-collapse: collapse;
}

tbody tr {
  border: none !important;
}

tbody td {
  border: none !important;
}
</style>

