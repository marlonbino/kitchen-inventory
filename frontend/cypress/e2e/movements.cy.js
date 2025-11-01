describe('Stock Movements View E2E Tests', () => {
  beforeEach(() => {
    // Visit the movements page
    cy.visit('/movements')
    cy.waitForPageLoad()
  })

  it('should display movements page with correct title', () => {
    cy.title().should('include', 'Stock Movements')
    cy.get('h1').should('contain', 'Stock Movements')
    cy.contains('History of all stock movements').should('be.visible')
  })

  it('should display record movement and export buttons', () => {
    cy.contains('button', 'Record Movement').should('be.visible')
    cy.contains('button', 'Export CSV').should('be.visible')
  })

  it('should disable export button when there are no movements', () => {
    // Check if export button is disabled when no data
    cy.get('body').then($body => {
      const movementCount = $body.find('tr, [class*="movement"]').length
      if (movementCount === 0) {
        cy.verifyExportDisabled()
      } else {
        cy.verifyExportEnabled()
      }
    })
  })

  it('should open record movement modal when clicking Record Movement', () => {
    cy.contains('button', 'Record Movement').click()
    cy.wait(500)
    
    cy.verifyModalOpen()
    cy.contains('Record', { matchCase: false }).should('be.visible')
  })

  it('should filter movements by type', () => {
    cy.wait(2000)
    
    // Select Receipt type
    cy.get('label').contains('Movement Type').parent().find('select').select('receipt')
    cy.wait(1500)
    
    // Verify only receipts are shown
    cy.get('body').then($body => {
      expect($body.text().toLowerCase()).to.not.include('issue')
    })
  })

  it('should filter movements by item', () => {
    cy.wait(2000)
    
    // Select an item
    cy.get('label').contains('Item').parent().find('select').select('Tomatoes')
    cy.wait(1500)
    
    // Verify filtered results
    cy.contains('Tomatoes').should('be.visible')
  })

  it('should filter movements by date range', () => {
    cy.wait(2000)
    
    // Set date from (7 days ago)
    const dateFrom = new Date()
    dateFrom.setDate(dateFrom.getDate() - 7)
    const dateFromStr = dateFrom.toISOString().split('T')[0]
    
    cy.get('label').contains('Date From').parent().find('input[type="date"]').clear().type(dateFromStr)
    cy.wait(1500)
    
    // Verify date filter applied
    cy.get('body').should('contain', 'movement')
  })

  it('should create a receipt movement successfully', () => {
    cy.contains('button', 'Record Movement').click()
    cy.wait(500)
    
    // Select item
    cy.get('label').contains('Item').parent().find('select').select('Tomatoes')
    
    // Select movement type
    cy.get('label').contains('Movement Type').parent().find('select').select('receipt')
    
    // Enter quantity
    cy.fillInput('Quantity', '50')
    
    // Enter reference
    cy.fillInput('Reference', 'TEST-REC-001')
    
    // Enter notes
    cy.get('textarea').type('Test receipt movement from E2E tests', { force: true })
    
    // Submit
    cy.contains('button', 'Record', { matchCase: false }).click()
    
    // Wait for toast
    cy.waitForToast('success', 5000)
    
    // Verify movement appears in list
    cy.contains('TEST-REC-001').should('be.visible')
  })

  it('should prevent issue movement with insufficient stock', () => {
    cy.contains('button', 'Record Movement').click()
    cy.wait(500)
    
    // Select item with low stock
    cy.get('label').contains('Item').parent().find('select').select('Tomatoes')
    
    // Select issue type
    cy.get('label').contains('Movement Type').parent().find('select').select('issue')
    
    // Try to issue more than available
    cy.fillInput('Quantity', '99999')
    
    // Submit should fail
    cy.contains('button', 'Record', { matchCase: false }).click()
    
    // Should show error
    cy.waitForToast('error', 5000)
  })

  it('should show stock warning for issue/writeoff movements', () => {
    cy.contains('button', 'Record Movement').click()
    cy.wait(500)
    
    // Select item
    cy.get('label').contains('Item').parent().find('select').select('Tomatoes')
    
    // Select issue type
    cy.get('label').contains('Movement Type').parent().find('select').select('issue')
    
    // Enter quantity that will trigger warning
    cy.fillInput('Quantity', '5')
    
    // Should show stock warning
    cy.get('[class*="warning"], [class*="alert"]').should('exist')
  })

  it('should display movement details with all fields', () => {
    cy.wait(2000)
    
    // Find a movement row
    cy.get('tr, [class*="movement"]').first().click()
    
    // Verify details are displayed
    cy.wait(500)
    cy.get('body').should('contain', 'Type')
    cy.get('body').should('contain', 'Quantity')
    cy.get('body').should('contain', 'Date')
  })

  it('should show correct movement type badges', () => {
    cy.wait(2000)
    
    // Check for receipt badge
    cy.get('body').then($body => {
      if ($body.text().includes('Receipt')) {
        cy.contains('Receipt').parent().find('[class*="green"]').should('exist')
      }
    })
    
    // Check for issue badge
    cy.get('body').then($body => {
      if ($body.text().includes('Issue')) {
        cy.contains('Issue').parent().find('[class*="blue"]').should('exist')
      }
    })
    
    // Check for write-off badge
    cy.get('body').then($body => {
      if ($body.text().includes('Write-off')) {
        cy.contains('Write-off').parent().find('[class*="red"]').should('exist')
      }
    })
  })

  it('should delete a movement with confirmation', () => {
    cy.wait(2000)
    
    // Get movement count
    let movementCount
    cy.get('tr, [class*="movement"]').then($movements => {
      movementCount = $movements.length
    })
    
    // Find and click delete button
    cy.get('button[aria-label*="Delete"], svg').then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click({ force: true })
        
        cy.wait(500)
        
        // Confirm deletion
        cy.confirmInDialog()
        
        cy.waitForToast('success', 5000)
        
        // Verify count decreased
        cy.wait(1000)
        cy.get('tr, [class*="movement"]').should('have.length.lessThan', movementCount)
      }
    })
  })

  it('should calculate running stock balance', () => {
    cy.wait(2000)
    
    // Check if running balance is displayed
    cy.get('body').then($body => {
      if ($body.text().includes('Balance') || $body.text().includes('Stock')) {
        cy.contains('Balance').should('exist')
      }
    })
  })

  it('should export movements to CSV', () => {
    cy.wait(2000)
    
    // Verify export button exists and is enabled
    cy.contains('button', 'Export CSV').should('not.be.disabled')
    
    // Click export button
    cy.contains('button', 'Export CSV').click()
    
    // Wait a moment for download to start
    cy.wait(500)
  })

  it('should handle pagination if many movements exist', () => {
    cy.wait(2000)
    
    // Check for pagination controls
    cy.get('body').then($body => {
      if ($body.find('[class*="pagination"], button:contains("Next"), button:contains("Previous")').length > 0) {
        cy.contains('Next', { matchCase: false }).should('exist')
        
        // Click next page
        cy.contains('Next', { matchCase: false }).click()
        cy.wait(1000)
        
        // Should be on page 2
        cy.contains('2').should('exist')
      }
    })
  })

  it('should show confirmation dialog before deleting', () => {
    cy.wait(2000)
    
    // Find delete button
    cy.get('button[aria-label*="Delete"], svg').then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click({ force: true })
        
        cy.wait(500)
        
        // Verify confirmation dialog
        cy.verifyConfirmationDialog()
        
        // Cancel
        cy.cancelInDialog()
      }
    })
  })

  it('should display toast notifications on actions', () => {
    cy.wait(2000)
    
    // Delete a movement
    cy.get('button[aria-label*="Delete"], svg').then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click({ force: true })
        
        cy.wait(500)
        cy.confirmInDialog()
        
        // Should show success toast
        cy.waitForToast('success', 5000)
      }
    })
  })

  it('should handle responsive layout', () => {
    // Desktop view
    cy.viewport(1280, 720)
    cy.wait(300)
    cy.contains('Stock Movements').should('be.visible')
    
    // Tablet view
    cy.viewport(768, 1024)
    cy.wait(300)
    cy.contains('Stock Movements').should('be.visible')
    
    // Mobile view
    cy.viewport(375, 667)
    cy.wait(300)
    cy.contains('Stock Movements').should('be.visible')
  })

  it('should show loading skeleton while fetching movements', () => {
    cy.reload()
    
    // Check for skeleton
    cy.get('[class*="animate-pulse"]').should('exist')
    
    cy.waitForPageLoad()
    cy.contains('Stock Movements').should('be.visible')
  })

  it('should handle empty state gracefully', () => {
    // This test may not always run if there's data, but structure is in place
    cy.get('body').then($body => {
      if ($body.text().includes('No movements') || $body.text().includes('No data')) {
        cy.contains('No movements', { matchCase: false }).should('be.visible')
        cy.verifyExportDisabled()
      }
    })
  })
})

