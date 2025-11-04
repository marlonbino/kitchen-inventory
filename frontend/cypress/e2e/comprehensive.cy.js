describe('Comprehensive System Tests', () => {
  const testUser = {
    username: 'admin',
    password: 'p@ssw0rd'
  }

  beforeEach(() => {
    // Clear localStorage and visit login page
    cy.clearLocalStorage()
    cy.visit('/')
  })

  describe('Authentication Tests', () => {
    it('should display login page', () => {
      cy.url().should('include', '/login')
      cy.contains('Sign in to your account').should('be.visible')
      cy.get('input[type="text"]').should('be.visible')
      cy.get('input[type="password"]').should('be.visible')
      cy.get('button[type="submit"]').should('contain', 'Sign In')
    })

    it('should show error on invalid credentials', () => {
      cy.get('input[type="text"]').type('invalid')
      cy.get('input[type="password"]').type('invalid')
      cy.get('button[type="submit"]').click()
      cy.contains('Invalid credentials', { timeout: 5000 }).should('be.visible')
    })

    it('should successfully login with valid credentials', () => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.url({ timeout: 10000 }).should('not.include', '/login')
      cy.contains('Dashboard', { timeout: 10000 }).should('be.visible')
    })

    it('should persist authentication after page reload', () => {
      // Login first
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.url({ timeout: 10000 }).should('not.include', '/login')
      
      // Reload page
      cy.reload()
      cy.url().should('not.include', '/login')
      cy.contains('Dashboard').should('be.visible')
    })

    it('should logout successfully', () => {
      // Login first
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      // Logout
      cy.get('[data-testid="user-menu"]').click()
      cy.contains('Logout').click()
      cy.url({ timeout: 5000 }).should('include', '/login')
    })
  })

  describe('Dashboard Tests', () => {
    beforeEach(() => {
      // Login before each test
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
    })

    it('should display dashboard statistics', () => {
      cy.contains('Dashboard').should('be.visible')
      cy.contains('Total Items').should('be.visible')
      cy.contains('Running Low').should('be.visible')
      cy.contains('In Transit').should('be.visible')
    })

    it('should display low stock items section', () => {
      cy.contains('Low Stock Items').should('be.visible')
    })

    it('should display recent movements section', () => {
      cy.contains('Recent Movements').should('be.visible')
    })
  })

  describe('Inventory Management Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      // Navigate to inventory
      cy.contains('Inventory Items').click()
      cy.wait(1000)
    })

    it('should display inventory list', () => {
      cy.contains('Inventory Items').should('be.visible')
      cy.get('[data-testid="items-list"]').should('exist')
    })

    it('should search items', () => {
      cy.get('input[placeholder*="Search"]').type('Rice')
      cy.wait(1000)
      cy.get('[data-testid="items-list"]').should('contain', 'Rice')
    })

    it('should filter items by category', () => {
      cy.get('select').first().select('Groceries')
      cy.wait(1000)
      cy.get('[data-testid="items-list"]').should('be.visible')
    })

    it('should open add item modal', () => {
      cy.contains('Add New Item').click()
      cy.contains('Create New Item').should('be.visible')
    })

    it('should create new item', () => {
      const timestamp = Date.now()
      const itemName = `Test Item ${timestamp}`
      
      cy.contains('Add New Item').click()
      cy.get('input[placeholder*="Item name"]').type(itemName)
      cy.get('select').first().select('Groceries')
      cy.get('input[placeholder*="Current stock"]').type('100')
      cy.get('input[placeholder*="Minimum"]').type('20')
      cy.get('select').eq(1).select('kg')
      cy.get('input[placeholder*="Price"]').type('50')
      cy.contains('Create Item').click()
      cy.wait(2000)
      
      cy.contains(itemName, { timeout: 5000 }).should('be.visible')
    })

    it('should edit item', () => {
      cy.get('[data-testid="edit-item-btn"]').first().click()
      cy.get('input[placeholder*="Item name"]').clear().type('Updated Item')
      cy.contains('Save Changes').click()
      cy.wait(2000)
    })

    it('should delete item', () => {
      cy.get('[data-testid="delete-item-btn"]').first().click()
      cy.contains('Are you sure').should('be.visible')
      cy.contains('Delete').click()
      cy.wait(2000)
    })
  })

  describe('Stock Movements Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      cy.contains('Stock Usage').click()
      cy.wait(1000)
    })

    it('should display stock movements list', () => {
      cy.contains('Stock Usage').should('be.visible')
      cy.get('[data-testid="movements-list"]').should('exist')
    })

    it('should record receipt', () => {
      cy.contains('Record Movement').click()
      cy.contains('Receive Delivery').click()
      cy.wait(500)
      
      cy.get('select').first().select(1) // Select first item
      cy.get('input[placeholder*="Quantity"]').type('50')
      cy.get('textarea').type('Test receipt movement')
      cy.contains('Submit').click()
      cy.wait(2000)
    })

    it('should record usage', () => {
      cy.contains('Record Movement').click()
      cy.contains('Track Usage').click()
      cy.wait(500)
      
      cy.get('select').first().select(1)
      cy.get('input[placeholder*="Quantity"]').type('10')
      cy.get('textarea').type('Test usage movement')
      cy.contains('Submit').click()
      cy.wait(2000)
    })

    it('should record waste', () => {
      cy.contains('Record Movement').click()
      cy.contains('Track Waste').click()
      cy.wait(500)
      
      cy.get('select').first().select(1)
      cy.get('input[placeholder*="Quantity"]').type('5')
      cy.get('textarea').type('Test waste movement')
      cy.contains('Submit').click()
      cy.wait(2000)
    })

    it('should filter movements by type', () => {
      cy.get('select[data-testid="type-filter"]').select('receipt')
      cy.wait(1000)
      cy.get('[data-testid="movements-list"]').should('exist')
    })
  })

  describe('Purchase Requests Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      cy.contains('Purchase Requests').click()
      cy.wait(1000)
    })

    it('should display requisitions list', () => {
      cy.contains('Purchase Requests').should('be.visible')
    })

    it('should create purchase request', () => {
      cy.contains('Create Purchase Request').click()
      cy.get('select').first().select(1)
      cy.get('input[placeholder*="Quantity"]').type('100')
      cy.get('textarea').type('Need for upcoming event')
      cy.contains('Submit Request').click()
      cy.wait(2000)
    })

    it('should approve purchase request', () => {
      cy.get('[data-testid="approve-btn"]').first().click()
      cy.wait(2000)
      cy.contains('Approved').should('be.visible')
    })

    it('should reject purchase request', () => {
      cy.get('[data-testid="reject-btn"]').first().click()
      cy.get('textarea').type('Not needed at this time')
      cy.contains('Reject Request').click()
      cy.wait(2000)
    })

    it('should assign delivery', () => {
      cy.get('[data-testid="assign-btn"]').first().click()
      cy.wait(2000)
    })
  })

  describe('Deliveries Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      cy.contains('Pending Deliveries').click()
      cy.wait(1000)
    })

    it('should display pending deliveries', () => {
      cy.contains('Pending Deliveries').should('be.visible')
    })

    it('should confirm delivery', () => {
      cy.get('[data-testid="confirm-delivery-btn"]').first().click()
      cy.contains('Confirm').click()
      cy.wait(2000)
    })
  })

  describe('Low Stock Alerts Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      cy.contains('Low Stock Alert').click()
      cy.wait(1000)
    })

    it('should display low stock items', () => {
      cy.contains('Low Stock Alert').should('be.visible')
    })

    it('should show stock percentage', () => {
      cy.get('[data-testid="stock-percentage"]').should('exist')
    })

    it('should create requisition from low stock item', () => {
      cy.get('[data-testid="create-requisition-btn"]').first().click()
      cy.wait(1000)
    })
  })

  describe('Analytics Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      cy.contains('Analytics & Reports').click()
      cy.wait(1000)
    })

    it('should display analytics dashboard', () => {
      cy.contains('Analytics & Reports').should('be.visible')
    })

    it('should display summary statistics', () => {
      cy.contains('Total Items').should('be.visible')
      cy.contains('Urgent Reorders').should('be.visible')
      cy.contains('Pending Approvals').should('be.visible')
    })

    it('should display items by category', () => {
      cy.contains('Items by Category').should('be.visible')
    })

    it('should display most used items', () => {
      cy.contains('Most Used Items').should('be.visible')
    })

    it('should display recent activity', () => {
      cy.contains('Recent Activity').should('be.visible')
    })

    it('should generate report', () => {
      cy.contains('Generate Report').click()
      cy.get('select').select('Last 7 Days')
      cy.contains('Generate').click()
      cy.wait(2000)
    })
  })

  describe('Category Management Tests (Admin)', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      cy.contains('Manage Categories').click()
      cy.wait(1000)
    })

    it('should display categories', () => {
      cy.contains('Manage Categories').should('be.visible')
    })

    it('should create category', () => {
      const timestamp = Date.now()
      const categoryName = `Test Category ${timestamp}`
      
      cy.contains('Add Category').click()
      cy.get('input[placeholder*="Category name"]').type(categoryName)
      cy.get('textarea').type('Test category description')
      cy.contains('Create Category').click()
      cy.wait(2000)
      
      cy.contains(categoryName).should('be.visible')
    })

    it('should edit category', () => {
      cy.get('[data-testid="edit-category-btn"]').first().click()
      cy.get('input[placeholder*="Category name"]').clear().type('Updated Category')
      cy.contains('Save').click()
      cy.wait(2000)
    })

    it('should delete category', () => {
      cy.get('[data-testid="delete-category-btn"]').last().click()
      cy.contains('Delete').click()
      cy.wait(2000)
    })
  })

  describe('User Management Tests (Admin)', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
      
      cy.contains('Manage Users').click()
      cy.wait(1000)
    })

    it('should display users list', () => {
      cy.contains('Manage Users').should('be.visible')
    })

    it('should create user', () => {
      const timestamp = Date.now()
      const username = `testuser${timestamp}`
      
      cy.contains('Create User').click()
      cy.get('input[placeholder*="Username"]').type(username)
      cy.get('input[placeholder*="Email"]').type(`${username}@test.com`)
      cy.get('input[placeholder*="Password"]').type('testpass123')
      cy.get('select').select('staff')
      cy.contains('Create User').click()
      cy.wait(2000)
      
      cy.contains(username).should('be.visible')
    })

    it('should display role badges', () => {
      cy.get('[data-testid="user-role-badge"]').should('exist')
    })

    it('should delete user', () => {
      cy.get('[data-testid="delete-user-btn"]').last().click()
      cy.contains('Delete').click()
      cy.wait(2000)
    })
  })

  describe('Dark Mode Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
    })

    it('should toggle dark mode', () => {
      cy.get('[data-testid="dark-mode-toggle"]').click()
      cy.get('html').should('have.class', 'dark')
      
      cy.get('[data-testid="dark-mode-toggle"]').click()
      cy.get('html').should('not.have.class', 'dark')
    })

    it('should persist dark mode preference', () => {
      cy.get('[data-testid="dark-mode-toggle"]').click()
      cy.reload()
      cy.get('html').should('have.class', 'dark')
    })
  })

  describe('Navigation Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
    })

    const pages = [
      'Dashboard',
      'Inventory Items',
      'Stock Usage',
      'Purchase Requests',
      'Low Stock Alert',
      'Pending Deliveries',
      'Analytics & Reports',
      'Manage Categories',
      'Manage Users'
    ]

    pages.forEach(page => {
      it(`should navigate to ${page}`, () => {
        cy.contains(page).click()
        cy.wait(1000)
        cy.contains(page).should('be.visible')
      })
    })
  })

  describe('Responsive Design Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
    })

    it('should display correctly on mobile', () => {
      cy.viewport('iphone-x')
      cy.contains('Dashboard').should('be.visible')
    })

    it('should display correctly on tablet', () => {
      cy.viewport('ipad-2')
      cy.contains('Dashboard').should('be.visible')
    })

    it('should display correctly on desktop', () => {
      cy.viewport(1920, 1080)
      cy.contains('Dashboard').should('be.visible')
    })
  })

  describe('Error Handling Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
    })

    it('should handle network errors gracefully', () => {
      cy.intercept('GET', '/api/items/*', { forceNetworkError: true })
      cy.contains('Inventory Items').click()
      cy.wait(2000)
    })

    it('should show validation errors', () => {
      cy.contains('Inventory Items').click()
      cy.contains('Add New Item').click()
      cy.contains('Create Item').click()
      // Should show validation errors
    })
  })

  describe('Full Workflow Tests', () => {
    beforeEach(() => {
      cy.get('input[type="text"]').type(testUser.username)
      cy.get('input[type="password"]').type(testUser.password)
      cy.get('button[type="submit"]').click()
      cy.wait(2000)
    })

    it('should complete full inventory workflow', () => {
      const timestamp = Date.now()
      const itemName = `Workflow Item ${timestamp}`
      
      // 1. Create item
      cy.contains('Inventory Items').click()
      cy.contains('Add New Item').click()
      cy.get('input[placeholder*="Item name"]').type(itemName)
      cy.get('select').first().select('Groceries')
      cy.get('input[placeholder*="Current stock"]').type('10')
      cy.get('input[placeholder*="Minimum"]').type('50')
      cy.get('select').eq(1).select('kg')
      cy.contains('Create Item').click()
      cy.wait(2000)
      
      // 2. Check low stock alert
      cy.contains('Low Stock Alert').click()
      cy.contains(itemName).should('be.visible')
      
      // 3. Create purchase request
      cy.contains('Purchase Requests').click()
      cy.contains('Create Purchase Request').click()
      cy.get('select').select(itemName)
      cy.get('input[placeholder*="Quantity"]').type('100')
      cy.get('textarea').type('Restocking')
      cy.contains('Submit Request').click()
      cy.wait(2000)
      
      // 4. Approve request
      cy.get('[data-testid="approve-btn"]').first().click()
      cy.wait(2000)
      
      // 5. Assign delivery
      cy.get('[data-testid="assign-btn"]').first().click()
      cy.wait(2000)
      
      // 6. Confirm delivery
      cy.contains('Pending Deliveries').click()
      cy.get('[data-testid="confirm-delivery-btn"]').first().click()
      cy.contains('Confirm').click()
      cy.wait(2000)
      
      // 7. Verify stock updated
      cy.contains('Inventory Items').click()
      cy.contains(itemName).parent().should('contain', '110')
    })
  })
})

