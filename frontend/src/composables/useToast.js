import { useToast as useVueToast } from 'vue-toastification'

/**
 * Centralized Toast Notification Composable
 * 
 * Provides consistent toast notifications across the application
 * with sensible defaults for each notification type.
 */
export const useToast = () => {
  const toast = useVueToast()

  /**
   * Show success notification
   * @param {string} message - Success message
   * @param {object} options - Additional toast options
   */
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

  /**
   * Show error notification
   * @param {string} message - Error message
   * @param {object} options - Additional toast options
   */
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

  /**
   * Show info notification
   * @param {string} message - Info message
   * @param {object} options - Additional toast options
   */
  const showInfo = (message, options = {}) => {
    return toast.info(message, {
      position: 'top-right',
      timeout: 3000,
      ...options
    })
  }

  /**
   * Show warning notification
   * @param {string} message - Warning message
   * @param {object} options - Additional toast options
   */
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

