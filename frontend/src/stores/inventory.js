import { defineStore } from 'pinia'
import {
  getItems,
  createItem as apiCreateItem,
  updateItem as apiUpdateItem,
  deleteItem as apiDeleteItem,
  getStockMovements,
  createStockMovement as apiCreateStockMovement,
  getRequisitions,
  createRequisition as apiCreateRequisition,
  approveRequisition as apiApproveRequisition,
  rejectRequisition as apiRejectRequisition,
  assignDelivery as apiAssignDelivery,
  confirmReceived as apiConfirmReceived,
  getLowStock,
  getDashboardStats
} from '../services/api'

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    // Items
    items: [],
    itemsCount: 0,
    itemsNext: null,
    itemsPrevious: null,
    
    // Stock Movements
    stockMovements: [],
    stockMovementsCount: 0,
    stockMovementsNext: null,
    stockMovementsPrevious: null,
    
    // Requisitions
    requisitions: [],
    requisitionsCount: 0,
    requisitionsNext: null,
    requisitionsPrevious: null,
    
    // Low Stock Items
    lowStockItems: [],
    
    // Dashboard Stats
    dashboardStats: null,
    
    // Loading states
    loading: {
      items: false,
      stockMovements: false,
      requisitions: false,
      lowStock: false,
      dashboardStats: false
    },
    
    // Error states
    error: {
      items: null,
      stockMovements: null,
      requisitions: null,
      lowStock: null,
      dashboardStats: null
    }
  }),

  getters: {
    /**
     * Get item by ID
     * @param {number} id - Item ID
     * @returns {Object|null} Item object or null
     */
    itemById: (state) => (id) => {
      return state.items.find(item => item.id === id) || null
    },

    /**
     * Get pending requisitions
     * @returns {Array} Array of pending requisitions
     */
    pendingRequisitions: (state) => {
      return state.requisitions.filter(req => req.status === 'pending')
    },

    /**
     * Get critical items (very low stock - below 50% of min_stock_level)
     * @returns {Array} Array of critical items
     */
    criticalItems: (state) => {
      return state.lowStockItems.filter(item => {
        const shortagePercent = ((item.min_stock_level - item.current_stock) / item.min_stock_level) * 100
        return shortagePercent >= 50
      })
    },

    /**
     * Get items by category
     * @param {string} category - Category name
     * @returns {Array} Array of items in category
     */
    itemsByCategory: (state) => (category) => {
      return state.items.filter(item => item.category_name === category)
    },

    /**
     * Get stock movements by item
     * @param {number} itemId - Item ID
     * @returns {Array} Array of movements for item
     */
    movementsByItem: (state) => (itemId) => {
      return state.stockMovements.filter(movement => movement.item_id === itemId)
    },

    /**
     * Get requisitions by item
     * @param {number} itemId - Item ID
     * @returns {Array} Array of requisitions for item
     */
    requisitionsByItem: (state) => (itemId) => {
      return state.requisitions.filter(req => req.item_id === itemId)
    }
  },

  actions: {
    // ==================== ITEMS ACTIONS ====================

    /**
     * Fetch items from API
     * @param {Object} params - Query parameters
     */
    async fetchItems(params = {}) {
      this.loading.items = true
      this.error.items = null
      
      try {
        const data = await getItems(params)
        this.items = data.results || data
        this.itemsCount = data.count || data.length
        this.itemsNext = data.next || null
        this.itemsPrevious = data.previous || null
      } catch (error) {
        this.error.items = error.userMessage || error.message || 'Failed to load items'
        throw error
      } finally {
        this.loading.items = false
      }
    },

    /**
     * Add a new item
     * @param {Object} itemData - Item data
     */
    async addItem(itemData) {
      try {
        const newItem = await apiCreateItem(itemData)
        this.items.push(newItem)
        this.itemsCount++
        return newItem
      } catch (error) {
        throw error
      }
    },

    /**
     * Update an existing item
     * @param {number} id - Item ID
     * @param {Object} itemData - Updated item data
     */
    async updateItem(id, itemData) {
      try {
        const updatedItem = await apiUpdateItem(id, itemData)
        const index = this.items.findIndex(item => item.id === id)
        if (index !== -1) {
          this.items[index] = updatedItem
        }
        return updatedItem
      } catch (error) {
        throw error
      }
    },

    /**
     * Delete an item
     * @param {number} id - Item ID
     */
    async removeItem(id) {
      try {
        await apiDeleteItem(id)
        this.items = this.items.filter(item => item.id !== id)
        this.itemsCount--
      } catch (error) {
        throw error
      }
    },

    // ==================== STOCK MOVEMENTS ACTIONS ====================

    /**
     * Fetch stock movements from API
     * @param {Object} params - Query parameters
     */
    async fetchStockMovements(params = {}) {
      this.loading.stockMovements = true
      this.error.stockMovements = null
      
      try {
        const data = await getStockMovements(params)
        this.stockMovements = data.results || data
        this.stockMovementsCount = data.count || data.length
        this.stockMovementsNext = data.next || null
        this.stockMovementsPrevious = data.previous || null
      } catch (error) {
        this.error.stockMovements = error.userMessage || error.message || 'Failed to load stock movements'
        throw error
      } finally {
        this.loading.stockMovements = false
      }
    },

    /**
     * Add a new stock movement
     * @param {Object} movementData - Movement data
     */
    async addStockMovement(movementData) {
      try {
        const newMovement = await apiCreateStockMovement(movementData)
        this.stockMovements.unshift(newMovement) // Add to beginning
        this.stockMovementsCount++
        
        // Update item stock in local state if item exists
        const item = this.itemById(movementData.item_id)
        if (item) {
          if (newMovement.movement_type === 'receipt') {
            item.current_stock += newMovement.quantity
          } else if (['usage', 'waste'].includes(newMovement.movement_type)) {
            // No change - tracking only
          }
        }
        
        return newMovement
      } catch (error) {
        throw error
      }
    },

    // ==================== REQUISITIONS ACTIONS ====================

    /**
     * Fetch requisitions from API
     * @param {Object} params - Query parameters
     */
    async fetchRequisitions(params = {}) {
      this.loading.requisitions = true
      this.error.requisitions = null
      
      try {
        const data = await getRequisitions(params)
        this.requisitions = data.results || data
        this.requisitionsCount = data.count || data.length
        this.requisitionsNext = data.next || null
        this.requisitionsPrevious = data.previous || null
      } catch (error) {
        this.error.requisitions = error.userMessage || error.message || 'Failed to load requisitions'
        throw error
      } finally {
        this.loading.requisitions = false
      }
    },

    /**
     * Create a new requisition
     * @param {Object} requisitionData - Requisition data
     */
    async createRequisition(requisitionData) {
      try {
        const newRequisition = await apiCreateRequisition(requisitionData)
        this.requisitions.unshift(newRequisition) // Add to beginning
        this.requisitionsCount++
        return newRequisition
      } catch (error) {
        throw error
      }
    },

    /**
     * Approve a requisition
     * @param {number} id - Requisition ID
     * @param {string} moneyReceivedBy - Name of person who received the money
     */
    async approveRequisition(id, moneyReceivedBy) {
      try {
        const updatedRequisition = await apiApproveRequisition(id, moneyReceivedBy)
        const index = this.requisitions.findIndex(req => req.id === id)
        if (index !== -1) {
          this.requisitions[index] = updatedRequisition
        }
        return updatedRequisition
      } catch (error) {
        throw error
      }
    },

    /**
     * Reject a requisition
     * @param {number} id - Requisition ID
     */
    async rejectRequisition(id) {
      try {
        const updatedRequisition = await apiRejectRequisition(id)
        const index = this.requisitions.findIndex(req => req.id === id)
        if (index !== -1) {
          this.requisitions[index] = updatedRequisition
        }
        return updatedRequisition
      } catch (error) {
        throw error
      }
    },

    /**
     * Assign delivery to a person
     * @param {number} id - Requisition ID
     * @param {string} assignedTo - Name of person assigned
     */
    async assignDelivery(id, assignedTo) {
      try {
        const updatedRequisition = await apiAssignDelivery(id, assignedTo)
        const index = this.requisitions.findIndex(req => req.id === id)
        if (index !== -1) {
          this.requisitions[index] = updatedRequisition
        }
        return updatedRequisition
      } catch (error) {
        throw error
      }
    },

    /**
     * Confirm receipt of items
     * @param {number} id - Requisition ID
     * @param {number} quantityReceived - Quantity actually received
     * @param {string} receiptNotes - Notes about receipt
     */
    async confirmReceived(id, quantityReceived, receiptNotes) {
      try {
        const updatedRequisition = await apiConfirmReceived(id, quantityReceived, receiptNotes)
        const index = this.requisitions.findIndex(req => req.id === id)
        if (index !== -1) {
          this.requisitions[index] = updatedRequisition
        }
        return updatedRequisition
      } catch (error) {
        throw error
      }
    },

    // ==================== LOW STOCK ACTIONS ====================

    /**
     * Fetch low stock items from API
     */
    async fetchLowStock() {
      this.loading.lowStock = true
      this.error.lowStock = null
      
      try {
        const data = await getLowStock()
        this.lowStockItems = data
      } catch (error) {
        this.error.lowStock = error.userMessage || error.message || 'Failed to load low stock items'
        throw error
      } finally {
        this.loading.lowStock = false
      }
    },

    // ==================== DASHBOARD STATS ACTIONS ====================

    /**
     * Fetch dashboard statistics
     */
    async fetchDashboardStats() {
      this.loading.dashboardStats = true
      this.error.dashboardStats = null
      
      try {
        const data = await getDashboardStats()
        this.dashboardStats = data
      } catch (error) {
        this.error.dashboardStats = error.userMessage || error.message || 'Failed to load dashboard statistics'
        throw error
      } finally {
        this.loading.dashboardStats = false
      }
    },

    // ==================== UTILITY ACTIONS ====================

    /**
     * Clear all state (useful for logout or reset)
     */
    clearAll() {
      this.items = []
      this.stockMovements = []
      this.requisitions = []
      this.lowStockItems = []
      this.dashboardStats = null
      this.itemsCount = 0
      this.stockMovementsCount = 0
      this.requisitionsCount = 0
    }
  }
})

