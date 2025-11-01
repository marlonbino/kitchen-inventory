// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

// Prevent Cypress from failing on uncaught exceptions
Cypress.on('uncaught:exception', (err, runnable) => {
  // Returning false here prevents Cypress from failing the test
  // on uncaught exceptions
  return false
})

// Global beforeEach hook to ensure API base URL is set
beforeEach(() => {
  // Ensure we're connecting to the correct backend
  const apiBaseUrl = Cypress.env('API_BASE_URL') || 'http://localhost:8000/api'
  
  cy.window().then((win) => {
    // Set API base URL in localStorage if needed
    win.localStorage.setItem('apiBaseUrl', apiBaseUrl)
  })
})

