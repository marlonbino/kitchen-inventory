# Quick Validation Checklist

## ⚡ 5-Minute Validation

Use this checklist to quickly validate the implementation:

### ✅ Backend Setup

```bash
# 1. Navigate to backend
cd kitchen-inventory/backend

# 2. Run seed command
python manage.py seed_test_data

# 3. Check output - should see:
# ✓ 5 items created
# ✓ 10 stock movements created  
# ✓ 3 requisitions created
# ✓ 2 low stock items detected
```

**Expected**: Success message with summary

---

### ✅ Frontend Setup

```bash
# 1. Navigate to frontend
cd kitchen-inventory/frontend

# 2. Install dependencies (if not done)
npm install

# 3. Check Cypress installation
npx cypress version

# 4. Verify test scripts exist
npm run test:e2e       # Should work
npm run test:e2e:open  # Should open GUI
```

**Expected**: No errors, Cypress v13 installed

---

### ✅ File Structure

Check these files exist:

**Backend**:
- [ ] `inventory/management/commands/seed_test_data.py`
- [ ] `inventory/fixtures/test_data_fixture.json`
- [ ] `TEST_DATA_SEEDER.md`
- [ ] `SEEDER_SUMMARY.md`

**Frontend**:
- [ ] `cypress.config.js`
- [ ] `cypress/support/commands.js`
- [ ] `cypress/support/e2e.js`
- [ ] `cypress/e2e/dashboard.cy.js`
- [ ] `cypress/e2e/items.cy.js`
- [ ] `cypress/e2e/movements.cy.js`
- [ ] `cypress/e2e/requisitions.cy.js`
- [ ] `cypress/e2e/integration.cy.js`
- [ ] `src/composables/useToast.js`
- [ ] `TOAST_AND_DIALOG_IMPLEMENTATION_PLAN.md`

**Expected**: All files present

---

### ✅ Test Execution

**Run Cypress in GUI mode** (recommended first time):

```bash
cd kitchen-inventory/frontend
npm run test:e2e:open
```

**In Cypress GUI**:
1. Click "E2E Testing"
2. Select your browser (Chrome recommended)
3. Click on `dashboard.cy.js`
4. Watch first test run
5. Check for toast notifications
6. Check for confirmation dialogs

**Expected**: Tests run successfully

---

### ✅ Quick Manual Checks

**1. Dashboard** (`http://localhost:5173`)
- [ ] Statistics cards show correct numbers
- [ ] Low stock alert visible
- [ ] Recent movements display
- [ ] Navigation works

**2. Items** (`/items`)
- [ ] 5 items visible
- [ ] Search works
- [ ] Filter by category works
- [ ] Low stock highlighted
- [ ] Add item shows toast
- [ ] Delete shows confirmation

**3. Movements** (`/movements`)
- [ ] 10 movements visible
- [ ] Filters work
- [ ] Record movement works
- [ ] Export button works
- [ ] Delete shows confirmation

**4. Requisitions** (`/requisitions`)
- [ ] 3 requisitions visible
- [ ] Tabs filter correctly
- [ ] Approve shows confirmation
- [ ] Reject shows confirmation
- [ ] Create works

**5. Low Stock** (`/low-stock`)
- [ ] 2 items visible
- [ ] Visual indicators present
- [ ] Quick actions work

---

## 🐛 Common Issues

### Issue: Cypress not installed
**Fix**: `npm install` in frontend directory

### Issue: Backend connection error
**Fix**: Ensure backend running on port 8000

### Issue: Tests fail to start
**Fix**: Check `baseUrl` in `cypress.config.js`

### Issue: Toast notifications not visible
**Fix**: Check `vue-toastification` installed

### Issue: Confirmation dialogs not showing
**Fix**: Check `ConfirmDialog.vue` imported correctly

---

## 📊 Success Indicators

You know it's working when:

✅ Seed command completes without errors
✅ Cypress GUI opens successfully
✅ Tests run without crashes
✅ Toast notifications appear on actions
✅ Confirmation dialogs show before deletes
✅ All 70+ tests pass
✅ Dashboard shows live data
✅ Low stock items are highlighted

---

## 🎯 Quick Test Run

**Minimal validation** (2 minutes):

```bash
# Terminal 1: Backend
cd kitchen-inventory/backend
python manage.py seed_test_data

# Terminal 2: Frontend + Test
cd kitchen-inventory/frontend
npm install
npm run test:e2e -- --spec "cypress/e2e/dashboard.cy.js"
```

**Expected**: Dashboard tests pass ✅

---

## 📝 Notes

- First `npm install` may take 2-3 minutes
- Cypress downloads on first run
- Backend must be running for E2E tests
- Test data auto-clears on seed re-run

---

**Status**: ✅ Ready to validate
**Time Required**: 5-10 minutes for full check

