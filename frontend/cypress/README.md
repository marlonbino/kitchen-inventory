# Cypress E2E Tests

End-to-end tests for the Kitchen Inventory System using Cypress.

## 🎯 Test Coverage

The test suite covers all major features of the Kitchen Inventory System:

### ✅ Dashboard Tests (`dashboard.cy.js`)
- Statistics cards with live data
- Low stock alerts
- Recent movements
- Navigation links
- Auto-refresh functionality
- Loading and error states
- Responsive layout

### ✅ Items View Tests (`items.cy.js`)
- Search and filter functionality
- Low stock highlighting
- Create, edit, delete operations
- Form validation
- Confirmation dialogs
- Responsive layout
- Toast notifications

### ✅ Stock Movements Tests (`movements.cy.js`)
- Filter by type, item, date range
- Create movements (receipt, issue, write-off)
- Stock validation and warnings
- Export to CSV
- Pagination
- Delete with confirmation
- Movement type badges
- Empty state handling

### ✅ Requisitions Tests (`requisitions.cy.js`)
- Status filtering (Pending, Approved, Rejected)
- Search functionality
- Create requisitions
- Approve/reject operations
- Bulk approve
- Statistics display
- Export functionality
- Toast notifications

### ✅ Integration Tests (`integration.cy.js`)
- Complete workflows across views
- Low stock alert workflows
- Navigation across app
- Toast notification consistency
- Responsive layout verification
- Form validation across forms

## 🚀 Setup

### 1. Install Dependencies

```bash
cd kitchen-inventory/frontend
npm install
```

This will install Cypress along with other dependencies.

### 2. Start Backend API

Make sure your Django backend is running with test data:

```bash
cd kitchen-inventory/backend
python manage.py seed_test_data
python manage.py runserver
```

### 3. Start Frontend

In a separate terminal:

```bash
cd kitchen-inventory/frontend
npm run dev
```

The frontend should be running on `http://localhost:5173`.

## 🧪 Running Tests

### Run All Tests in Headless Mode

```bash
npm run test:e2e
```

### Open Cypress Test Runner

```bash
npm run test:e2e:open
```

This opens the Cypress Test Runner GUI where you can:
- Select tests to run
- Watch tests run in real-time
- Debug tests
- See screenshots and videos

### Run Specific Test File

```bash
# Using Cypress CLI
npx cypress run --spec "cypress/e2e/dashboard.cy.js"
```

## 📋 Prerequisites

Before running tests, ensure:

1. ✅ **Backend is running** on `http://localhost:8000`
2. ✅ **Frontend is running** on `http://localhost:5173`
3. ✅ **Test data is seeded** using `python manage.py seed_test_data`
4. ✅ **Database is clean** (seeder clears existing data)

## 🔧 Configuration

Cypress configuration is in `cypress.config.js`:

```javascript
{
  e2e: {
    baseUrl: 'http://localhost:5173',
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 10000
  }
}
```

## 🛠️ Custom Commands

Custom commands are defined in `cypress/support/commands.js`:

- `waitForPageLoad()` - Wait for page load and API calls
- `waitForToast()` - Wait for toast notifications
- `clickAndWaitForToast()` - Click button and wait for toast
- `navigateTo()` - Navigate to a route
- `fillInput()` - Fill a form input by label
- `selectOption()` - Select from dropdown
- `clickButton()` - Click button by text
- `verifyModalOpen()` - Verify modal is open
- `verifyLowStock()` - Verify low stock indicator
- `verifyConfirmationDialog()` - Verify confirmation dialog
- `confirmInDialog()` - Confirm in dialog
- `cancelInDialog()` - Cancel in dialog
- `verifyExportDisabled()` - Verify export is disabled
- `verifyExportEnabled()` - Verify export is enabled
- And more...

## 📊 Test Data

Tests use data seeded by `seed_test_data` command:

- **5 Items**: Tomatoes (LOW), Milk, Rice, Chicken Breast (LOW), Black Pepper
- **10 Stock Movements**: Mix of receipts, issues, and write-offs
- **3 Requisitions**: One pending, one approved, one rejected

## 🐛 Troubleshooting

### Tests Fail to Connect

**Problem**: Tests can't connect to frontend or backend.

**Solution**: 
- Ensure frontend is running on `http://localhost:5173`
- Ensure backend is running on `http://localhost:8000`
- Check `cypress.config.js` baseUrl

### Tests Time Out

**Problem**: Tests timeout waiting for elements.

**Solution**:
- Increase timeout in `cypress.config.js`
- Check if API calls are slow
- Verify test data is loaded

### Element Not Found

**Problem**: Tests can't find elements.

**Solution**:
- Run tests in GUI mode to see what's rendered
- Check if selectors match actual DOM
- Use `cy.get('body').debug()` to inspect DOM

### API Errors

**Problem**: Tests fail with API errors.

**Solution**:
- Verify backend is running
- Check if test data is seeded
- Look at Network tab in browser dev tools
- Check backend logs

### Flaky Tests

**Problem**: Tests pass sometimes but fail other times.

**Solution**:
- Add proper waits: `cy.waitForPageLoad()`
- Use `cy.wait()` with appropriate timeouts
- Check for race conditions
- Increase timeout values

## 📸 Screenshots and Videos

Failed tests automatically generate:
- Screenshot on failure
- Video of entire test run

These are saved to:
- `cypress/screenshots/`
- `cypress/videos/`

## 🔍 Debugging Tips

1. **Use Cypress GUI**: Open with `npm run test:e2e:open` for interactive debugging
2. **Add `.then()` logs**: `cy.get('selector').then(($el) => console.log($el))`
3. **Pause execution**: Add `cy.pause()` in test
4. **Inspect DOM**: Use `cy.get('body').debug()`
5. **Check network**: Use `cy.intercept()` to spy on API calls

## 📝 Writing New Tests

When adding new tests:

1. Follow existing test patterns
2. Use custom commands when possible
3. Add proper waits for async operations
4. Test both success and error paths
5. Include responsive layout checks
6. Verify toast notifications
7. Use descriptive test names

Example:

```javascript
describe('New Feature Tests', () => {
  beforeEach(() => {
    cy.visit('/new-feature')
    cy.waitForPageLoad()
  })

  it('should display new feature correctly', () => {
    cy.get('h1').should('contain', 'New Feature')
    cy.contains('Expected text').should('be.visible')
  })

  it('should handle user interaction', () => {
    cy.contains('button', 'Click Me').click()
    cy.waitForToast('success', 5000)
    cy.contains('Expected result').should('be.visible')
  })
})
```

## 🎯 CI/CD Integration

To run in CI/CD:

```yaml
# Example GitHub Actions
- name: Run Cypress tests
  run: |
    cd kitchen-inventory/frontend
    npm run test:e2e
```

Make sure to:
- Install dependencies
- Start backend server
- Start frontend server
- Run migrations and seed data

## 📚 Resources

- [Cypress Documentation](https://docs.cypress.io/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [Custom Commands](https://docs.cypress.io/api/cypress-api/custom-commands)
- [Intercepting Network Requests](https://docs.cypress.io/api/commands/intercept)

## ✅ Test Checklist

Before committing:

- [ ] All tests pass in headless mode
- [ ] All tests pass in GUI mode
- [ ] No flaky tests
- [ ] Screenshots/Videos reviewed for failures
- [ ] Test coverage is comprehensive
- [ ] Custom commands are used appropriately
- [ ] Error handling is tested
- [ ] Responsive layout is verified
- [ ] Toast notifications are verified
- [ ] Form validations are tested

## 🤝 Contributing

When adding new features:
1. Add corresponding E2E tests
2. Follow existing test patterns
3. Update this README if needed
4. Ensure tests pass before PR

## 📞 Support

For issues with tests:
1. Check troubleshooting section
2. Review Cypress documentation
3. Check existing tests for patterns
4. Open an issue with details

