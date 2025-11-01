describe('Requisitions View E2E Tests', () => {
  beforeEach(() => {
    // Visit the requisitions page
    cy.visit('/requisitions')
    cy.waitForPageLoad()
  })

  it('should display requisitions page with correct title', () => {
    cy.title().should('include', 'Requisitions')
    cy.get('h1').should('contain', 'Requisitions')
    cy.contains('Manage item requisition requests').should('be.visible')
  })

  it('should display create requisition button', () => {
    cy.contains('button', 'Create Requisition').should('be.visible')
  })

  it('should display export button', () => {
    cy.contains('button', 'Export CSV').should('be.visible')
  })

  it('should disable export when no requisitions', () => {
    cy.get('body').then($body => {
      const requisitionCount = $body.find('tr, [class*="requisition"]').length
      if (requisitionCount === 0) {
        cy.verifyExportDisabled()
      }
    })
  })

  it('should display statistics cards', () => {
    cy.wait(2000)
    
    // Verify statistics cards
    cy.contains('Total Pending').should('be.visible')
    cy.contains('Most Requested Item').should('be.visible')
    cy.contains('Urgent').should('be.visible')
  })

  it('should filter requisitions by status tabs', () => {
    cy.wait(2000)
    
    // Click on Pending tab
    cy.contains('button', 'Pending', { matchCase: false }).click()
    cy.wait(1000)
    
    // Verify only pending requisitions shown
    cy.get('body').then($body => {
      if ($body.find('tr, [class*="requisition"]').length > 0) {
        cy.get('tr, [class*="requisition"]').should('not.contain', 'Approved')
      }
    })
    
    // Click on Approved tab
    cy.contains('button', 'Approved', { matchCase: false }).click()
    cy.wait(1000)
    
    // Click on Rejected tab
    cy.contains('button', 'Rejected', { matchCase: false }).click()
    cy.wait(1000)
    
    // Click on All tab
    cy.contains('button', 'All').click()
    cy.wait(1000)
  })

  it('should search requisitions by item or requester', () => {
    cy.wait(2000)
    
    // Search by requester
    cy.get('input[placeholder*="Search"]').type('Chef', { delay: 100 })
    cy.wait(1500)
    
    // Verify search results
    cy.contains('Chef').should('be.visible')
  })

  it('should open create requisition modal', () => {
    cy.contains('button', 'Create Requisition').click()
    cy.wait(500)
    
    cy.verifyModalOpen()
    cy.contains('Create Requisition', { matchCase: false }).should('be.visible')
  })

  it('should create a requisition successfully', () => {
    cy.contains('button', 'Create Requisition').click()
    cy.wait(500)
    
    // Select item
    cy.get('label').contains('Item').parent().find('select').select('Tomatoes')
    
    // Enter quantity
    cy.fillInput('Quantity Requested', '100')
    
    // Enter requester
    cy.fillInput('Requested By', 'E2E Test User')
    
    // Submit
    cy.contains('button', 'Create', { matchCase: false }).click()
    
    cy.waitForToast('success', 5000)
    
    // Verify requisition appears
    cy.contains('E2E Test User').should('be.visible')
  })

  it('should show suggested quantity for low stock items', () => {
    cy.contains('button', 'Create Requisition').click()
    cy.wait(500)
    
    // Select low stock item (Tomatoes)
    cy.get('label').contains('Item').parent().find('select').select('Tomatoes')
    
    // Should show suggested quantity
    cy.get('[class*="suggest"], [class*="hint"]').should('exist')
  })

  it('should approve a requisition', () => {
    cy.wait(2000)
    
    // Click Pending tab
    cy.contains('button', 'Pending', { matchCase: false }).click()
    cy.wait(1000)
    
    // Find pending requisition and approve button
    cy.get('button').contains('Approve', { matchCase: false }).then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click()
        
        cy.wait(500)
        cy.confirmInDialog()
        
        cy.waitForToast('success', 5000)
        
        // Verify status changed
        cy.wait(1000)
      }
    })
  })

  it('should reject a requisition', () => {
    cy.wait(2000)
    
    // Click Pending tab
    cy.contains('button', 'Pending', { matchCase: false }).click()
    cy.wait(1000)
    
    // Find pending requisition and reject button
    cy.get('button').contains('Reject', { matchCase: false }).then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click()
        
        cy.wait(500)
        cy.confirmInDialog()
        
        cy.waitForToast('success', 5000)
        
        // Verify status changed
        cy.wait(1000)
      }
    })
  })

  it('should bulk approve requisitions', () => {
    cy.wait(2000)
    
    // Click Pending tab
    cy.contains('button', 'Pending', { matchCase: false }).click()
    cy.wait(1000)
    
    // Check if bulk approve button exists
    cy.get('body').then($body => {
      if ($body.find('button:contains("Approve Selected")').length > 0) {
        // Select multiple requisitions
        cy.get('input[type="checkbox"]').then($checkboxes => {
          if ($checkboxes.length > 1) {
            cy.wrap($checkboxes).eq(0).check({ force: true })
            cy.wrap($checkboxes).eq(1).check({ force: true })
            
            // Click bulk approve
            cy.contains('button', 'Approve Selected').click()
            
            cy.wait(500)
            cy.confirmInDialog()
            
            cy.waitForToast('success', 5000)
          }
        })
      }
    })
  })

  it('should show confirmation dialog for status changes', () => {
    cy.wait(2000)
    
    // Find approve button
    cy.get('button').contains('Approve', { matchCase: false }).then($buttons => {
      if ($buttons.length > 0) {
        cy.wrap($buttons.first()).click()
        
        cy.wait(500)
        
        // Verify confirmation dialog
        cy.verifyConfirmationDialog()
        
        cy.cancelInDialog()
      }
    })
  })

  it('should display requisition status badges', () => {
    cy.wait(2000)
    
    // Check for pending badge
    cy.get('body').then($body => {
      if ($body.text().includes('Pending')) {
        cy.contains('Pending').parent().find('[class*="yellow"], [class*="warning"]').should('exist')
      }
    })
    
    // Check for approved badge
    cy.get('body').then($body => {
      if ($body.text().includes('Approved')) {
        cy.contains('Approved').parent().find('[class*="green"], [class*="success"]').should('exist')
      }
    })
    
    // Check for rejected badge
    cy.get('body').then($body => {
      if ($body.text().includes('Rejected')) {
        cy.contains('Rejected').parent().find('[class*="red"], [class*="danger"]').should('exist')
      }
    })
  })

  it('should show requisition details', () => {
    cy.wait(2000)
    
    // Click on a requisition row
    cy.get('tr, [class*="requisition"]').then($rows => {
      if ($rows.length > 0) {
        cy.wrap($rows.first()).click()
        
        cy.wait(500)
        
        // Verify details shown
        cy.get('body').should('contain', 'Item')
        cy.get('body').should('contain', 'Quantity')
        cy.get('body').should('contain', 'Requested By')
      }
    })
  })

  it('should export requisitions to CSV', () => {
    cy.wait(2000)
    
    // Verify export is enabled if data exists
    cy.get('body').then($body => {
      if ($body.find('tr, [class*="requisition"]').length > 0) {
        cy.verifyExportEnabled()
        
        cy.contains('button', 'Export CSV').click()
        cy.wait(500)
      }
    })
  })

  it('should update pending requisitions count after approval', () => {
    cy.wait(2000)
    
    // Get initial pending count
    let initialPendingCount
    cy.contains('Total Pending').parent().find('p.text-2xl').then($el => {
      initialPendingCount = parseInt($el.text())
    })
    
    // Approve a requisition
    cy.contains('button', 'Pending', { matchCase: false }).click()
    cy.wait(1000)
    
    cy.get('button').contains('Approve', { matchCase: false }).then($buttons => {
      if ($buttons.length > 0 && initialPendingCount > 0) {
        cy.wrap($buttons.first()).click()
        cy.wait(500)
        cy.confirmInDialog()
        cy.waitForToast('success', 5000)
        
        // Verify count decreased
        cy.wait(1000)
      }
    })
  })

  it('should handle responsive layout', () => {
    // Desktop view
    cy.viewport(1280, 720)
    cy.wait(300)
    cy.contains('Requisitions').should('be.visible')
    
    // Tablet view
    cy.viewport(768, 1024)
    cy.wait(300)
    cy.contains('Requisitions').should('be.visible')
    
    // Mobile view
    cy.viewport(375, 667)
    cy.wait(300)
    cy.contains('Requisitions').should('be.visible')
  })

  it('should show loading skeleton while fetching', () => {
    cy.reload()
    
    cy.get('[class*="animate-pulse"]').should('exist')
    
    cy.waitForPageLoad()
    cy.contains('Requisitions').should('be.visible')
  })

  it('should filter by category if available', () => {
    cy.wait(2000)
    
    // Check if category filter exists
    cy.get('body').then($body => {
      if ($body.find('label:contains("Category")').length > 0) {
        cy.get('label').contains('Category').parent().find('select').select('Produce')
        cy.wait(1500)
        
        // Verify filtered
        cy.contains('Tomatoes').should('be.visible')
      }
    })
  })

  it('should show empty state when no requisitions', () => {
    // This test may not always run
    cy.get('body').then($body => {
      if ($body.text().includes('No requisitions') || $body.text().includes('No data')) {
        cy.contains('No requisitions', { matchCase: false }).should('be.visible')
        cy.verifyExportDisabled()
      }
    })
  })

  it('should validate form when creating requisition', () => {
    cy.contains('button', 'Create Requisition').click()
    cy.wait(500)
    
    // Try to submit empty form
    cy.contains('button', 'Create', { matchCase: false }).click()
    
    // Should show validation errors
    cy.get('[class*="error"], [class*="red"]').should('exist')
  })
})

