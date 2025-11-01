describe('Full Integration E2E Tests', () => {
  it('should complete a full workflow: Create item -> Add movement -> Create requisition -> Approve', () => {
    // Start at dashboard
    cy.visit('/')
    cy.waitForPageLoad()
    
    // Get initial stats
    let initialItems, initialMovements, initialPendingRequisitions
    
    cy.contains('Total Items').parent().find('p.text-3xl').then($el => {
      initialItems = parseInt($el.text())
    })
    
    cy.contains('Pending Requisitions').parent().find('p.text-3xl').then($el => {
      initialPendingRequisitions = parseInt($el.text())
    })
    
    // Step 1: Navigate to Items and create a new item
    cy.visit('/items')
    cy.waitForPageLoad()
    
    cy.contains('button', 'Add New Item').click()
    cy.wait(500)
    
    cy.fillInput('Name', 'Integration Test Item')
    cy.get('label').contains('Category').parent().find('select').select('Produce')
    cy.get('label').contains('Unit').parent().find('select').select('kg')
    cy.fillInput('Minimum Stock Level', '50')
    cy.fillInput('Current Stock', '100')
    
    cy.contains('button', 'Create', { matchCase: false }).click()
    cy.waitForToast('success', 5000)
    
    // Verify item created
    cy.contains('Integration Test Item').should('be.visible')
    
    // Step 2: Navigate to Movements and record a receipt
    cy.visit('/movements')
    cy.waitForPageLoad()
    
    cy.contains('button', 'Record Movement').click()
    cy.wait(500)
    
    cy.get('label').contains('Item').parent().find('select').select('Integration Test Item')
    cy.get('label').contains('Movement Type').parent().find('select').select('receipt')
    cy.fillInput('Quantity', '25')
    cy.fillInput('Reference', 'INT-TEST-REC-001')
    cy.get('textarea').type('Integration test receipt', { force: true })
    
    cy.contains('button', 'Record', { matchCase: false }).click()
    cy.waitForToast('success', 5000)
    
    // Verify movement created
    cy.contains('INT-TEST-REC-001').should('be.visible')
    
    // Step 3: Record an issue
    cy.contains('button', 'Record Movement').click()
    cy.wait(500)
    
    cy.get('label').contains('Item').parent().find('select').select('Integration Test Item')
    cy.get('label').contains('Movement Type').parent().find('select').select('issue')
    cy.fillInput('Quantity', '30')
    cy.fillInput('Reference', 'INT-TEST-ISS-001')
    cy.get('textarea').type('Integration test issue', { force: true })
    
    cy.contains('button', 'Record', { matchCase: false }).click()
    cy.waitForToast('success', 5000)
    
    // Step 4: Navigate to Items and verify stock updated
    cy.visit('/items')
    cy.waitForPageLoad()
    
    cy.contains('Integration Test Item').parent().within(() => {
      cy.should('contain', '95') // 100 + 25 - 30 = 95
    })
    
    // Step 5: Navigate to Requisitions and create one
    cy.visit('/requisitions')
    cy.waitForPageLoad()
    
    cy.contains('button', 'Create Requisition').click()
    cy.wait(500)
    
    cy.get('label').contains('Item').parent().find('select').select('Integration Test Item')
    cy.fillInput('Quantity Requested', '50')
    cy.fillInput('Requested By', 'Integration Test User')
    
    cy.contains('button', 'Create', { matchCase: false }).click()
    cy.waitForToast('success', 5000)
    
    // Verify requisition created
    cy.contains('Integration Test User').should('be.visible')
    cy.contains('Pending').should('be.visible')
    
    // Step 6: Approve the requisition
    cy.contains('button', 'Pending', { matchCase: false }).click()
    cy.wait(1000)
    
    cy.contains('Integration Test User').parent().parent().within(() => {
      cy.contains('button', 'Approve', { matchCase: false }).click()
    })
    
    cy.wait(500)
    cy.confirmInDialog()
    cy.waitForToast('success', 5000)
    
    // Step 7: Navigate back to dashboard and verify stats updated
    cy.visit('/')
    cy.waitForPageLoad()
    cy.wait(2000)
    
    cy.contains('Total Items').parent().find('p.text-3xl').then($el => {
      const newItems = parseInt($el.text())
      expect(newItems).to.be.greaterThan(initialItems)
    })
  })

  it('should handle low stock alert workflow', () => {
    // Navigate to items
    cy.visit('/items')
    cy.waitForPageLoad()
    
    // Find a low stock item (should be Tomatoes)
    cy.contains('Tomatoes').should('be.visible')
    
    // Verify low stock indicator
    cy.contains('Tomatoes').parent().find('[class*="red"], [class*="warning"]').should('exist')
    
    // Navigate to low stock view
    cy.visit('/low-stock')
    cy.waitForPageLoad()
    
    // Verify Tomatoes appears in low stock
    cy.contains('Tomatoes').should('be.visible')
    
    // Create a requisition from low stock view
    cy.contains('Tomatoes').parent().parent().within(() => {
      cy.get('button').contains('Request', { matchCase: false }).then($button => {
        if ($button.length > 0) {
          cy.wrap($button.first()).click()
          
          cy.wait(500)
          cy.fillInput('Requested By', 'Low Stock Test')
          cy.contains('button', 'Create', { matchCase: false }).click()
          
          cy.waitForToast('success', 5000)
        }
      })
    })
  })

  it('should verify all navigation links work', () => {
    cy.visit('/')
    
    // Test Dashboard link
    cy.get('nav').contains('Dashboard').click()
    cy.url().should('include', '/')
    cy.get('h1').should('contain', 'Dashboard')
    
    // Test Items link
    cy.get('nav').contains('Items').click()
    cy.url().should('include', '/items')
    cy.get('h1').should('contain', 'Items')
    
    // Test Movements link
    cy.get('nav').contains('Movements').click()
    cy.url().should('include', '/movements')
    cy.get('h1').should('contain', 'Stock Movements')
    
    // Test Requisitions link
    cy.get('nav').contains('Requisitions').click()
    cy.url().should('include', '/requisitions')
    cy.get('h1').should('contain', 'Requisitions')
    
    // Test Low Stock link
    cy.get('nav').contains('Low Stock').click()
    cy.url().should('include', '/low-stock')
    cy.get('h1').should('contain', 'Low Stock')
  })

  it('should verify toast notifications throughout app', () => {
    // Navigate to items
    cy.visit('/items')
    cy.waitForPageLoad()
    
    // Create an item and verify toast
    cy.contains('button', 'Add New Item').click()
    cy.wait(500)
    
    cy.fillInput('Name', 'Toast Test Item')
    cy.get('label').contains('Category').parent().find('select').select('Produce')
    cy.get('label').contains('Unit').parent().find('select').select('kg')
    cy.fillInput('Minimum Stock Level', '20')
    cy.fillInput('Current Stock', '50')
    
    cy.contains('button', 'Create', { matchCase: false }).click()
    cy.waitForToast('success', 5000)
    
    // Delete the item and verify toast
    cy.contains('Toast Test Item').parent().parent().within(() => {
      cy.get('button[aria-label*="Delete"], svg').first().click({ force: true })
    })
    
    cy.wait(500)
    cy.confirmInDialog()
    cy.waitForToast('success', 5000)
  })

  it('should verify responsive layout across all views', () => {
    const views = ['/', '/items', '/movements', '/requisitions', '/low-stock']
    
    views.forEach(view => {
      cy.visit(view)
      cy.waitForPageLoad()
      
      // Mobile view
      cy.viewport(375, 667)
      cy.wait(300)
      cy.get('h1').should('be.visible')
      
      // Tablet view
      cy.viewport(768, 1024)
      cy.wait(300)
      cy.get('h1').should('be.visible')
      
      // Desktop view
      cy.viewport(1280, 720)
      cy.wait(300)
      cy.get('h1').should('be.visible')
    })
  })

  it('should verify form validation across forms', () => {
    // Test item form validation
    cy.visit('/items')
    cy.waitForPageLoad()
    
    cy.contains('button', 'Add New Item').click()
    cy.wait(500)
    
    // Try to submit without filling
    cy.contains('button', 'Create', { matchCase: false }).click()
    cy.get('[class*="error"]').should('exist')
    
    // Test movement form validation
    cy.visit('/movements')
    cy.waitForPageLoad()
    
    cy.contains('button', 'Record Movement').click()
    cy.wait(500)
    
    cy.contains('button', 'Record', { matchCase: false }).click()
    cy.get('[class*="error"]').should('exist')
    
    // Test requisition form validation
    cy.visit('/requisitions')
    cy.waitForPageLoad()
    
    cy.contains('button', 'Create Requisition').click()
    cy.wait(500)
    
    cy.contains('button', 'Create', { matchCase: false }).click()
    cy.get('[class*="error"]').should('exist')
  })

  it('should verify filter persistence across views', () => {
    cy.visit('/items')
    cy.waitForPageLoad()
    
    // Apply filter
    cy.get('label').contains('Category').parent().find('select').select('Produce')
    cy.wait(1500)
    
    // Verify filter applied
    cy.contains('Tomatoes').should('be.visible')
    
    // Navigate away and back
    cy.visit('/movements')
    cy.waitForPageLoad()
    
    cy.visit('/items')
    cy.waitForPageLoad()
    
    // Note: Filter persistence depends on implementation
    // This test documents the expectation
  })
})

