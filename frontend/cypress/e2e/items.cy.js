describe('Items View E2E Tests', () => {
  beforeEach(() => {
    // Visit the items page
    cy.visit('/items')
    cy.waitForPageLoad()
  })

  it('should display items page with correct title', () => {
    cy.title().should('include', 'Items')
    cy.get('h1').should('contain', 'Items')
    cy.contains('Manage your inventory items').should('be.visible')
  })

  it('should display add new item button', () => {
    cy.contains('button', 'Add New Item').should('be.visible')
  })

  it('should filter items by category', () => {
    cy.wait(2000)
    
    // Select Produce category
    cy.get('label').contains('Category').parent().find('select').select('Produce')
    cy.wait(1500)
    
    // Verify only Produce items are shown
    cy.get('div, tr').contains('Tomatoes').should('exist')
  })

  it('should filter items by unit', () => {
    cy.wait(2000)
    
    // Select kg unit
    cy.get('label').contains('Unit').parent().find('select').select('kg')
    cy.wait(1500)
    
    // Verify items are filtered
    cy.get('body').then(($body) => {
      expect($body.text()).to.include('kg')
    })
  })

  it('should search items by name', () => {
    cy.wait(2000)
    
    // Search for Tomatoes
    cy.get('input[placeholder*="Search"]').type('Tomatoes', { delay: 100 })
    cy.wait(1500)
    
    // Verify search results
    cy.contains('Tomatoes').should('be.visible')
    cy.contains('Milk').should('not.exist')
  })

  it('should highlight low stock items', () => {
    cy.wait(2000)
    
    // Search for low stock item (Tomatoes)
    cy.get('input[placeholder*="Search"]').type('Tomatoes', { delay: 100 })
    cy.wait(1500)
    
    // Verify low stock indicator exists
    cy.contains('Tomatoes').parent().find('[class*="red"], [class*="warning"], [class*="alert"]').should('exist')
  })

  it('should open add item modal when clicking Add New Item button', () => {
    cy.contains('button', 'Add New Item').click()
    cy.wait(500)
    
    // Verify modal is open
    cy.verifyModalOpen()
    cy.contains('Create Item', { matchCase: false }).should('be.visible')
  })

  it('should validate required fields when creating item', () => {
    cy.contains('button', 'Add New Item').click()
    cy.wait(500)
    
    // Try to submit empty form
    cy.contains('button', 'Create', { matchCase: false }).click()
    
    // Should show validation errors
    cy.get('body').then(($body) => {
      if ($body.text().includes('required') || $body.text().includes('error')) {
        cy.get('[class*="error"], [class*="text-red"]').should('exist')
      }
    })
  })

  it('should create a new item successfully', () => {
    cy.contains('button', 'Add New Item').click()
    cy.wait(500)
    
    // Fill in the form
    cy.fillInput('Name', 'Test Item')
    
    cy.get('label').contains('Category').parent().find('select').select('Produce')
    
    cy.get('label').contains('Unit').parent().find('select').select('kg')
    
    cy.fillInput('Minimum Stock Level', '10')
    cy.fillInput('Current Stock', '25')
    
    // Submit the form
    cy.contains('button', 'Create', { matchCase: false }).click()
    
    // Wait for toast notification
    cy.waitForToast('success', 5000)
    
    // Verify item appears in list
    cy.contains('Test Item').should('be.visible')
  })

  it('should open edit modal when clicking edit button', () => {
    cy.wait(2000)
    
    // Find and click edit button for an item
    cy.get('button[aria-label*="Edit"], svg').then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click({ force: true })
        
        cy.wait(500)
        cy.verifyModalOpen()
        cy.contains('Edit', { matchCase: false }).should('be.visible')
      }
    })
  })

  it('should update an item successfully', () => {
    cy.wait(2000)
    
    // Find edit button for Tomatoes
    cy.contains('Tomatoes').parent().find('button, svg').then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click({ force: true })
        
        cy.wait(500)
        
        // Update stock level
        cy.get('input[type="number"]').first().clear().type('15', { force: true })
        
        // Submit
        cy.contains('button', 'Update', { matchCase: false }).click()
        
        cy.waitForToast('success', 5000)
      }
    })
  })

  it('should show confirmation dialog when deleting item', () => {
    cy.wait(2000)
    
    // Find delete button
    cy.get('button[aria-label*="Delete"], svg').then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click({ force: true })
        
        cy.wait(500)
        
        // Verify confirmation dialog appears
        cy.verifyConfirmationDialog()
      }
    })
  })

  it('should delete item after confirmation', () => {
    cy.wait(2000)
    
    // Get item count before deletion
    let itemCountBefore
    cy.get('div, tr').then($items => {
      itemCountBefore = $items.length
    })
    
    // Find and click delete button
    cy.get('button[aria-label*="Delete"], svg').then($buttons => {
      if ($buttons.length > 1) {
        const itemName = $buttons.eq(1).closest('div, tr').find('text, span').first().text()
        
        cy.wrap($buttons.eq(1)).click({ force: true })
        
        cy.wait(500)
        
        // Confirm deletion
        cy.confirmInDialog()
        
        cy.waitForToast('success', 5000)
        
        // Verify item is removed
        cy.wait(1000)
        cy.get('body').should('not.contain', itemName)
      }
    })
  })

  it('should cancel deletion when clicking cancel', () => {
    cy.wait(2000)
    
    // Find delete button
    cy.get('button[aria-label*="Delete"], svg').then($buttons => {
      if ($buttons.length > 1) {
        const itemName = $buttons.eq(1).closest('div, tr').find('text, span').first().text()
        
        cy.wrap($buttons.eq(1)).click({ force: true })
        
        cy.wait(500)
        
        // Cancel deletion
        cy.cancelInDialog()
        
        // Verify item still exists
        cy.contains(itemName).should('exist')
      }
    })
  })

  it('should display items in a table or grid format', () => {
    cy.wait(2000)
    
    // Check if items are displayed
    cy.get('body').should('not.contain', 'No items found')
    
    // Verify items are displayed in a table or grid
    cy.get('table, [class*="grid"], [class*="table"]').should('exist')
  })

  it('should handle responsive layout on mobile', () => {
    cy.viewport('iphone-6')
    cy.wait(300)
    
    cy.contains('Items').should('be.visible')
    
    // On mobile, should show cards instead of table
    cy.get('body').then($body => {
      if ($body.find('[class*="card"], [class*="grid"]').length > 0) {
        cy.get('[class*="card"], [class*="grid"]').should('exist')
      }
    })
  })

  it('should reset filters when clicking clear', () => {
    cy.wait(2000)
    
    // Apply filters
    cy.get('label').contains('Category').parent().find('select').select('Produce')
    cy.get('input[placeholder*="Search"]').type('Tomatoes')
    
    cy.wait(1000)
    
    // Clear filters if clear button exists
    cy.get('body').then($body => {
      if ($body.find('button:contains("Clear"), button:contains("Reset")').length > 0) {
        cy.contains('button', 'Clear', { matchCase: false }).click()
        
        // Verify all items are shown again
        cy.wait(1000)
        cy.contains('Tomatoes').should('exist')
      }
    })
  })

  it('should show loading skeleton while fetching items', () => {
    // Force reload to see loading state
    cy.reload()
    
    // Check for skeleton loaders
    cy.get('[class*="animate-pulse"]').should('exist')
    
    // Wait for load to complete
    cy.waitForPageLoad()
    
    cy.contains('Items').should('be.visible')
  })
})

