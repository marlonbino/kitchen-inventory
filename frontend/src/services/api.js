import axios from 'axios';

// Create axios instance with base URL
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Helper to parse Django REST Framework errors
const parseApiError = (error) => {
  if (error.response) {
    const { data, status } = error.response;
    let message = 'An unknown error occurred.';

    if (status >= 500) {
      return 'A server error occurred. Please try again later.';
    }

    if (status === 400) { // Bad Request
      const errors = [];
      for (const key in data) {
        if (Array.isArray(data[key])) {
          errors.push(`${key}: ${data[key].join(' ')}`);
        }
      }
      if (errors.length > 0) {
        return errors.join('\n');
      }
    }

    if (typeof data === 'string') {
      message = data;
    } else if (data.detail) {
      message = data.detail;
    } else if (data.message) {
      message = data.message;
    } else if (data.error) {
      message = data.error;
    }

    return message;
  } else if (error.request) {
    return 'No response from server. Please check your network connection.';
  } else {
    return error.message || 'An unexpected error occurred.';
  }
};


// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    error.userMessage = parseApiError(error);
    return Promise.reject(error);
  }
);

// ==================== ITEMS API ====================

/**
 * Get all items with optional filters
 * @param {Object} params - Query parameters (category, unit, search, ordering, page)
 * @returns {Promise} Response with items data
 */
export const getItems = async (params = {}) => {
  const response = await apiClient.get('/items/', { params });
  return response.data;
};

/**
 * Create a new item
 * @param {Object} data - Item data (name, category, unit, min_stock_level, current_stock)
 * @returns {Promise} Created item data
 */
export const createItem = async (data) => {
  const response = await apiClient.post('/items/', data);
  return response.data;
};

/**
 * Update an existing item
 * @param {number} id - Item ID
 * @param {Object} data - Updated item data
 * @returns {Promise} Updated item data
 */
export const updateItem = async (id, data) => {
  const response = await apiClient.put(`/items/${id}/`, data);
  return response.data;
};

/**
 * Partially update an item
 * @param {number} id - Item ID
 * @param {Object} data - Partial item data
 * @returns {Promise} Updated item data
 */
export const patchItem = async (id, data) => {
  const response = await apiClient.patch(`/items/${id}/`, data);
  return response.data;
};

/**
 * Delete an item
 * @param {number} id - Item ID
 * @returns {Promise} Empty response
 */
export const deleteItem = async (id) => {
  const response = await apiClient.delete(`/items/${id}/`);
  return response.data;
};

/**
 * Get a single item by ID
 * @param {number} id - Item ID
 * @returns {Promise} Item data
 */
export const getItem = async (id) => {
  const response = await apiClient.get(`/items/${id}/`);
  return response.data;
};

// ==================== STOCK MOVEMENTS API ====================

/**
 * Get all stock movements with optional filters
 * @param {Object} params - Query parameters (movement_type, item, ordering, page)
 * @returns {Promise} Response with stock movements data
 */
export const getStockMovements = async (params = {}) => {
  const response = await apiClient.get('/stock-movements/', { params });
  return response.data;
};

/**
 * Create a new stock movement
 * @param {Object} data - Movement data (item_id, movement_type, quantity, notes, reference)
 * @returns {Promise} Created movement data
 */
export const createStockMovement = async (data) => {
  const response = await apiClient.post('/stock-movements/', data);
  return response.data;
};

/**
 * Get a single stock movement by ID
 * @param {number} id - Movement ID
 * @returns {Promise} Movement data
 */
export const getStockMovement = async (id) => {
  const response = await apiClient.get(`/stock-movements/${id}/`);
  return response.data;
};

/**
 * Update a stock movement
 * @param {number} id - Movement ID
 * @param {Object} data - Updated movement data
 * @returns {Promise} Updated movement data
 */
export const updateStockMovement = async (id, data) => {
  const response = await apiClient.put(`/stock-movements/${id}/`, data);
  return response.data;
};

/**
 * Delete a stock movement
 * @param {number} id - Movement ID
 * @returns {Promise} Empty response
 */
export const deleteStockMovement = async (id) => {
  const response = await apiClient.delete(`/stock-movements/${id}/`);
  return response.data;
};

// ==================== REQUISITIONS API ====================

/**
 * Get all requisitions with optional filters
 * @param {Object} params - Query parameters (status, item, ordering, page)
 * @returns {Promise} Response with requisitions data
 */
export const getRequisitions = async (params = {}) => {
  const response = await apiClient.get('/requisitions/', { params });
  return response.data;
};

/**
 * Create a new requisition
 * @param {Object} data - Requisition data (item_id, quantity_requested, requested_by, status)
 * @returns {Promise} Created requisition data
 */
export const createRequisition = async (data) => {
  const response = await apiClient.post('/requisitions/', data);
  return response.data;
};

/**
 * Get a single requisition by ID
 * @param {number} id - Requisition ID
 * @returns {Promise} Requisition data
 */
export const getRequisition = async (id) => {
  const response = await apiClient.get(`/requisitions/${id}/`);
  return response.data;
};

/**
 * Approve a requisition
 * @param {number} id - Requisition ID
 * @returns {Promise} Updated requisition data
 */
export const approveRequisition = async (id) => {
  const response = await apiClient.post(`/requisitions/${id}/approve/`);
  return response.data;
};

/**
 * Reject a requisition
 * @param {number} id - Requisition ID
 * @returns {Promise} Updated requisition data
 */
export const rejectRequisition = async (id) => {
  const response = await apiClient.post(`/requisitions/${id}/reject/`);
  return response.data;
};

/**
 * Update a requisition
 * @param {number} id - Requisition ID
 * @param {Object} data - Updated requisition data
 * @returns {Promise} Updated requisition data
 */
export const updateRequisition = async (id, data) => {
  const response = await apiClient.put(`/requisitions/${id}/`, data);
  return response.data;
};

/**
 * Delete a requisition
 * @param {number} id - Requisition ID
 * @returns {Promise} Empty response
 */
export const deleteRequisition = async (id) => {
  const response = await apiClient.delete(`/requisitions/${id}/`);
  return response.data;
};

// ==================== LOW STOCK API ====================

/**
 * Get all items with low stock levels
 * @returns {Promise} Array of low stock items
 */
export const getLowStock = async () => {
  const response = await apiClient.get('/low-stock/');
  return response.data;
};

// ==================== DASHBOARD STATS API ====================

/**
 * Get dashboard statistics
 * @returns {Promise} Dashboard stats data
 */
export const getDashboardStats = async () => {
  const response = await apiClient.get('/dashboard-stats/');
  return response.data;
};

export default apiClient;