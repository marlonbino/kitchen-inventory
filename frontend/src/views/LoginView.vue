<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-neutral-900 dark:to-neutral-800 px-4 py-12">
    <div class="w-full max-w-md">
      <div class="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-neutral-700">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="flex justify-center mb-4">
            <img :src="bitzLogo" alt="BITZ Logo" class="h-16 w-auto">
          </div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Kitchen System</h1>
          <p class="text-gray-600 dark:text-gray-400">Sign in to your account</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div v-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>

          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Username
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white transition-colors"
              placeholder="Enter your username"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="w-full px-4 py-3 border border-gray-300 dark:border-neutral-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-neutral-700 text-gray-900 dark:text-white transition-colors"
              placeholder="Enter your password"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Signing in...</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <!-- Security Notice -->
        <div class="mt-6 text-center">
          <p class="text-xs text-gray-500 dark:text-gray-400">
            🔒 Access is restricted. Contact your administrator for credentials.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login as apiLogin } from '../services/api.js'
import bitzLogo from '../assets/bitz-logo.svg'

const router = useRouter()
const route = useRoute()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await apiLogin(form.value)
    console.log('Login successful:', response)
    
    // Store auth token
    if (response.token) {
      localStorage.setItem('auth_token', response.token)
    }
    
    // Store user info in localStorage (optional, for display purposes)
    if (response.user) {
      localStorage.setItem('user', JSON.stringify(response.user))
    }
    
    // Navigate to dashboard or the original destination
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (err) {
    console.error('Login error:', err)
    error.value = err.userMessage || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

