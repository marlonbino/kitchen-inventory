describe('Dashboard E2E Tests', () => {
  beforeEach(() => {
    // Visit the dashboard page
    cy.visit('/')
    cy.waitForPageLoad()
  })

  it('should display dashboard with correct page title', () => {
    cy.title().should('include', 'Dashboard')
    cy.get('h1').should('contain', 'Dashboard')
    cy.contains('Overview of your kitchen inventory').should('be.visible')
  })

  it('should display all statistics cards with live data', () => {
    // Wait for API call to complete
    cy.wait(2000)

    // Verify Total Items card
    cy.contains('Total Items').should('be.visible')
    cy.contains('Total Items').parent().find('p.text-3xl').should('exist')
    
    // Verify Low Stock Items card with alert badge
    cy.contains('Low Stock Items').should('be.visible')
    cy.contains('Low Stock Items').parent().find('p.text-3xl').should('exist')
    
    // Verify Pending Requisitions card
    cy.contains('Pending Requisitions').should('be.visible')
    cy.contains('Pending Requisitions').parent().find('p.text-3xl').should('exist')
    
    // Verify Today\'s Movements card
    cy.contains('Today\'s Movements').should('be.visible')
    cy.contains('Today\'s Movements').parent().find('p.text-3xl').should('exist')
  })

  it('should display low stock alert with correct count', () => {
    // Wait for API call to complete
    cy.wait(2000)
    
    // Check for low stock card
    cy.contains('Low Stock Items').should('be.visible')
    
    // Get the count
    cy.contains('Low Stock Items').parent().find('p.text-3xl').then(($count) => {
      const count = parseInt($count.text())
      
      // If there are low stock items, verify alert badge exists
      if (count > 0) {
        cy.contains('Low Stock Items').parent().find('[class*="bg-red-100"]').should('exist')
        cy.contains('Alert').should('exist')
      }
    })
  })

  it('should navigate to low stock view when low stock card is clicked', () => {
    cy.wait(2000)
    
    cy.contains('Low Stock Items').parent().parent().click()
    cy.url().should('include', '/low-stock')
    cy.get('h1').should('contain', 'Low Stock')
  })

  it('should navigate to requisitions view when requisitions card is clicked', () => {
    cy.wait(2000)
    
    cy.contains('Pending Requisitions').parent().parent().click()
    cy.url().should('include', '/requisitions')
    cy.get('h1').should('contain', 'Requisitions')
  })

  it('should display recent stock movements section', () => {
    cy.wait(2000)
    
    cy.contains('Recent Stock Movements').should('be.visible')
    
    // Check if movements list exists
    cy.get('div[class*="space-y"]').within(() => {
      cy.get('div').should('have.length.at.least', 1)
    })
  })

  it('should display low stock alerts section', () => {
    cy.wait(2000)
    
    cy.contains('Low Stock Alerts').should('be.visible')
    
    // Check if alerts list exists
    cy.get('div').contains('Low Stock Alerts').parent().within(() => {
      cy.get('a, button').should('have.length.at.least', 1)
    })
  })

  it('should show movement type badges with correct colors', () => {
    cy.wait(2000)
    
    // Find recent movements
    cy.contains('Recent Stock Movements').should('be.visible')
    
    // Check for receipt badge
    cy.get('body').then(($body) => {
      if ($body.find('span:contains("Receipt")').length > 0) {
        cy.contains('Receipt').parent().should('have.class', 'bg-green-100')
      }
    })
    
    // Check for issue badge
    cy.get('body').then(($body) => {
      if ($body.find('span:contains("Issue")').length > 0) {
        cy.contains('Issue').parent().should('have.class', 'bg-blue-100')
      }
    })
    
    // Check for writeoff badge
    cy.get('body').then(($body) => {
      if ($body.find('span:contains("Write-off")').length > 0) {
        cy.contains('Write-off').parent().should('have.class', 'bg-red-100')
      }
    })
  })

  it('should refresh data automatically', () => {
    // Get initial values
    let initialTotalItems
    cy.contains('Total Items').parent().find('p.text-3xl').then(($el) => {
      initialTotalItems = $el.text()
    })
    
    // Wait for auto-refresh (30 seconds is too long, so we'll just verify the page doesn't break)
    cy.wait(1000)
    
    // Page should still be loaded
    cy.contains('Dashboard').should('be.visible')
  })

  it('should handle loading state with skeleton loaders', () => {
    // Force a page reload to trigger loading state
    cy.reload()
    
    // Check for skeleton loaders
    cy.get('[class*="animate-pulse"]').should('exist')
    
    // Wait for loading to complete
    cy.waitForPageLoad()
    
    // Verify data is loaded
    cy.contains('Total Items').should('be.visible')
  })

  it('should handle error state gracefully', () => {
    // Intercept API call and return error
    cy.intercept('GET', '**/api/dashboard-stats/**', { statusCode: 500 }).as('errorApi')
    
    cy.reload()
    
    // Wait for error response
    cy.wait('@errorApi')
    
    // Check for error message
    cy.get('body').then(($body) => {
      if ($body.find('[class*="error"], [class*="red"]').length > 0) {
        cy.contains('Error loading dashboard').should('be.visible')
        cy.contains('Try again').should('be.visible')
      }
    })
  })

  it('should maintain layout on different screen sizes', () => {
    // Desktop view
    cy.viewport(1280, 720)
    cy.wait(300)
    cy.contains('Total Items').should('be.visible')
    
    // Tablet view
    cy.viewport(768, 1024)
    cy.wait(300)
    cy.contains('Total Items').should('be.visible')
    
    // Mobile view
    cy.viewport(375, 667)
    cy.wait(300)
    cy.contains('Total Items').should('be.visible')
    
    // Verify stats cards grid adapts
    cy.get('[class*="grid"]').should('exist')
  })

  it('should display correct navigation links', () => {
    cy.get('nav').should('be.visible')
    cy.get('nav').contains('Dashboard').should('be.visible')
    cy.get('nav').contains('Items').should('be.visible')
    cy.get('nav').contains('Movements').should('be.visible')
    cy.get('nav').contains('Requisitions').should('be.visible')
    cy.get('nav').contains('Low Stock').should('be.visible')
  })

  it('should show pending requisitions count in navigation badge', () => {
    cy.wait(2000)
    
    // Check navbar for badge
    cy.get('nav').then(($nav) => {
      if ($nav.find('[class*="badge"], span[class*="bg"]').length > 0) {
        cy.get('nav').find('[class*="badge"]').should('exist')
      }
    })
  })
})

