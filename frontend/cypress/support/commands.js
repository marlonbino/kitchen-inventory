// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

/**
 * Custom command to wait for page to load and API calls to complete
 */
Cypress.Commands.add('waitForPageLoad', () => {
  // Wait for skeleton loaders to disappear
  cy.get('[class*="animate-pulse"]').should('not.exist')
  
  // Wait for any loading spinners to disappear
  cy.get('.loading-spinner, [data-testid="loading"]').should('not.exist')
})

/**
 * Custom command to wait for toast notifications
 */
Cypress.Commands.add('waitForToast', (message, timeout = 5000) => {
  cy.get('.Vue-Toastification__toast', { timeout }).should('be.visible')
  if (message) {
    cy.get('.Vue-Toastification__toast').contains(message)
  }
})

/**
 * Custom command to click a button and wait for toast
 */
Cypress.Commands.add('clickAndWaitForToast', (buttonSelector, expectedToast, timeout = 5000) => {
  cy.get(buttonSelector).click()
  cy.waitForToast(expectedToast, timeout)
})

/**
 * Custom command to navigate to a route
 */
Cypress.Commands.add('navigateTo', (route) => {
  cy.visit(route)
  cy.wait(500) // Wait for navigation
  cy.waitForPageLoad()
})

/**
 * Custom command to intercept API calls and wait for them
 */
Cypress.Commands.add('waitForApiCall', (method, url) => {
  cy.intercept(method, url).as('apiCall')
  cy.wait('@apiCall', { timeout: 10000 })
})

/**
 * Custom command to fill a form input
 */
Cypress.Commands.add('fillInput', (label, value) => {
  cy.contains('label', label).parent().find('input, select, textarea').clear().type(value)
})

/**
 * Custom command to select an option from a select
 */
Cypress.Commands.add('selectOption', (label, optionText) => {
  cy.contains('label', label).parent().find('select').select(optionText)
})

/**
 * Custom command to click a button by text
 */
Cypress.Commands.add('clickButton', (buttonText) => {
  cy.contains('button', buttonText).click()
})

/**
 * Custom command to verify modal is open
 */
Cypress.Commands.add('verifyModalOpen', (title) => {
  cy.get('[role="dialog"], .modal, [class*="modal"]').should('be.visible')
  if (title) {
    cy.contains(title).should('be.visible')
  }
})

/**
 * Custom command to close modal
 */
Cypress.Commands.add('closeModal', () => {
  cy.get('[role="dialog"] button[aria-label="Close"], button:contains("Cancel")').first().click()
})

/**
 * Custom command to verify low stock indicator
 */
Cypress.Commands.add('verifyLowStock', (itemName) => {
  cy.contains(itemName).parent().find('[class*="red"], [class*="warning"], [class*="alert"]').should('exist')
})

/**
 * Custom command to verify confirmation dialog
 */
Cypress.Commands.add('verifyConfirmationDialog', (message) => {
  cy.get('[role="dialog"]', { timeout: 5000 }).should('be.visible')
  if (message) {
    cy.contains(message).should('be.visible')
  }
})

/**
 * Custom command to confirm action in dialog
 */
Cypress.Commands.add('confirmInDialog', () => {
  cy.contains('button', 'Confirm', { timeout: 5000 }).click()
})

/**
 * Custom command to cancel action in dialog
 */
Cypress.Commands.add('cancelInDialog', () => {
  cy.contains('button', 'Cancel', { timeout: 5000 }).click()
})

/**
 * Custom command to verify export button is disabled
 */
Cypress.Commands.add('verifyExportDisabled', () => {
  cy.contains('button', 'Export').should('be.disabled')
})

/**
 * Custom command to verify export button is enabled
 */
Cypress.Commands.add('verifyExportEnabled', () => {
  cy.contains('button', 'Export').should('not.be.disabled')
})

/**
 * Custom command to check responsive layout
 */
Cypress.Commands.add('checkResponsive', () => {
  // Test mobile view
  cy.viewport('iphone-6')
  cy.wait(300)
  
  // Test tablet view
  cy.viewport('ipad-2')
  cy.wait(300)
  
  // Test desktop view
  cy.viewport(1280, 720)
  cy.wait(300)
})

/**
 * Custom command to seed test data by calling backend
 */
Cypress.Commands.add('seedTestData', () => {
  cy.request('POST', 'http://localhost:8000/api/seed-test-data/').then((response) => {
    expect(response.status).to.eq(200)
  })
})

/**
 * Custom command to wait for data table to load
 */
Cypress.Commands.add('waitForTable', () => {
  cy.get('table, [class*="table"], [class*="grid"]').should('be.visible')
  cy.waitForPageLoad()
})

/**
 * Override type command to add delay
 */
Cypress.Commands.overwrite('type', (originalFn, element, text, options) => {
  options = options || {}
  options.delay = options.delay === undefined ? 50 : options.delay
  return originalFn(element, text, options)
})

