import { ref, onMounted, watch } from 'vue'

const isDarkMode = ref(false)
const isSystemDark = ref(false)

export function useTheme() {
  // Initialize theme based on system preference or localStorage
  const initTheme = () => {
    // Check localStorage first
    const savedTheme = localStorage.getItem('theme')
    
    if (savedTheme === 'dark' || savedTheme === 'light') {
      isDarkMode.value = savedTheme === 'dark'
      updateTheme(isDarkMode.value)
    } else {
      // Check system preference
      isSystemDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      isDarkMode.value = isSystemDark.value
      updateTheme(isDarkMode.value)
    }

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      isSystemDark.value = e.matches
      const savedTheme = localStorage.getItem('theme')
      // Only update if user hasn't manually set a preference
      if (!savedTheme) {
        isDarkMode.value = e.matches
        updateTheme(e.matches)
      }
    })
  }

  // Update theme class on document
  const updateTheme = (dark) => {
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Toggle theme
  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
    updateTheme(isDarkMode.value)
  }

  // Set specific theme
  const setTheme = (theme) => {
    if (theme === 'dark' || theme === 'light') {
      isDarkMode.value = theme === 'dark'
      localStorage.setItem('theme', theme)
      updateTheme(isDarkMode.value)
    }
  }

  // Initialize on mount
  onMounted(() => {
    initTheme()
  })

  return {
    isDarkMode,
    toggleTheme,
    setTheme,
    initTheme
  }
}

