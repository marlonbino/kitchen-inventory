import { ref, watch } from 'vue'
import { debounce } from '../utils/debounce'

/**
 * Composable for debouncing reactive values
 * @param {Ref} source - Source reactive value to debounce
 * @param {number} delay - Delay in milliseconds (default: 300)
 * @returns {Ref} Debounced reactive value
 */
export function useDebounce(source, delay = 300) {
  const debounced = ref(source.value)

  const updateDebounced = debounce((value) => {
    debounced.value = value
  }, delay)

  watch(source, (newValue) => {
    updateDebounced(newValue)
  })

  return debounced
}

