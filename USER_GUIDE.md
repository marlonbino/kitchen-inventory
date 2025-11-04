# 📚 BITZ Kitchen Inventory System - User Guide

> **A Simple Guide for Everyone**  
> Learn how to manage your kitchen inventory in minutes!

---

## 📖 Table of Contents

1. [Getting Started](#-getting-started)
2. [User Roles](#-user-roles)
3. [Daily Workflows](#-daily-workflows)
4. [Step-by-Step Guides](#-step-by-step-guides)
5. [Common Tasks](#-common-tasks)
6. [Tips & Best Practices](#-tips--best-practices)
7. [Troubleshooting](#-troubleshooting)

---

## 🚀 Getting Started

### What is This System?

The BITZ Kitchen Inventory System helps you:
- **Track** what items you have in stock
- **Know** when to reorder items
- **Request** purchases when stock is low
- **Monitor** how items are used
- **Generate** reports for management

### First Time Login

1. **Open** your web browser
2. **Go to** the system URL (provided by your admin)
3. **Enter** your username and password
4. **Click** "Sign In"

```
┌─────────────────────────────┐
│   BITZ Kitchen System       │
│                             │
│   Username: [________]      │
│   Password: [________]      │
│                             │
│   [    Sign In    ]         │
└─────────────────────────────┘
```

---

## 👥 User Roles

### 🔵 Admin (Kitchen Manager)
**Can do everything:**
- ✅ Add/edit/delete items
- ✅ Approve purchase requests
- ✅ Manage users
- ✅ Generate reports
- ✅ View all activities

### 🟢 Staff (Kitchen Worker)
**Can do most tasks:**
- ✅ View inventory
- ✅ Record usage
- ✅ Create purchase requests
- ✅ Receive deliveries
- ❌ Cannot approve requests
- ❌ Cannot manage users

---

## 🔄 Daily Workflows

### Workflow 1: **Using Items** (Daily)

```
START
  │
  ├─► Open "Stock Movements"
  │
  ├─► Click "Record Movement"
  │
  ├─► Select Item (e.g., "Rice")
  │
  ├─► Choose "Usage"
  │
  ├─► Enter Quantity (e.g., "5 kg")
  │
  ├─► Add Notes (e.g., "Lunch prep")
  │
  ├─► Click "Save"
  │
  └─► ✅ Stock Updated Automatically
```

### Workflow 2: **Requesting Items** (When Low Stock)

```
START
  │
  ├─► Open "Purchase Requests"
  │
  ├─► Click "Request Item"
  │
  ├─► Select Item (e.g., "Sugar")
  │
  ├─► Enter Quantity Needed (e.g., "20 kg")
  │
  ├─► Enter Estimated Cost (e.g., "KSh 2,000")
  │
  ├─► Add Notes (optional)
  │
  ├─► Click "Submit Request"
  │
  ├─► Request sent to Admin 📧
  │
  └─► Wait for Approval
         │
         ├─► If APPROVED ✅
         │   │
         │   ├─► Money Released
         │   │
         │   ├─► Buy Item
         │   │
         │   └─► Record Receipt (see Workflow 3)
         │
         └─► If REJECTED ❌
             └─► See reason in notes
```

### Workflow 3: **Receiving Items** (After Purchase)

```
START
  │
  ├─► Items Delivered 📦
  │
  ├─► Open "Stock Movements"
  │
  ├─► Click "Record Movement"
  │
  ├─► Select Item
  │
  ├─► Choose "Receipt"
  │
  ├─► Enter Quantity Received
  │
  ├─► Add Notes (e.g., "Supplier: XYZ")
  │
  ├─► Click "Save"
  │
  └─► ✅ Stock Increased Automatically
```

### Workflow 4: **Approving Requests** (Admin Only)

```
START
  │
  ├─► Open "Purchase Requests"
  │
  ├─► See "Pending" tab (Red badge shows count)
  │
  ├─► Click on a Request
  │
  ├─► Review Details:
  │   ├─► Item needed
  │   ├─► Quantity
  │   ├─► Cost estimate
  │   └─► Who requested it
  │
  ├─► Decision Time:
  │   │
  │   ├─► APPROVE ✅
  │   │   │
  │   │   ├─► Enter who received the money
  │   │   │
  │   │   ├─► Click "Approve"
  │   │   │
  │   │   └─► Money released to buyer
  │   │
  │   └─► REJECT ❌
  │       │
  │       ├─► Enter reason
  │       │
  │       └─► Click "Reject"
  │
  └─► ✅ Requester Notified
```

---

## 📝 Step-by-Step Guides

### Guide 1: **How to Add a New Item** (Admin)

1. **Click** "Inventory" in the menu
2. **Click** "Add New Item" (+ button)
3. **Fill in** the details:
   - **Name**: e.g., "Cooking Oil"
   - **Category**: Choose from dropdown (e.g., "Groceries")
   - **Unit**: e.g., "litre"
   - **Current Stock**: e.g., "10"
   - **Minimum Level**: e.g., "5" (system alerts when below this)
   - **Unit Cost**: e.g., "500" (per litre)
4. **Click** "Save"
5. **Done!** Item appears in inventory

### Guide 2: **How to Check Low Stock Items**

1. **Look** at the Dashboard (home page)
2. **Find** the red "Urgent Reorders" card
3. **Click** on it to see list
4. **Or** go to "Inventory" and look for items with:
   - 🔴 Red highlight
   - Low percentage bar
5. **Create** purchase requests for these items

### Guide 3: **How to Generate a Report** (Admin)

1. **Click** "Statistics" in menu
2. **Click** "Generate Report" button
3. **Choose** time period:
   - Today
   - Last 7 Days
   - Last 30 Days
   - All Time
4. **Select** purchase request status filter:
   - All Requests
   - Pending Only
   - Approved Only
   - etc.
5. **Click** "Generate & Print"
6. **Report Opens** in new window
7. **Print** or Save as PDF

### Guide 4: **How to Create a Category** (Admin)

1. **Click** "Inventory" in menu
2. **Click** "Categories" tab
3. **Click** "Add Category" button
4. **Enter** category name (e.g., "Spices")
5. **Click** "Save"
6. **Use** this category when adding items

---

## ✨ Common Tasks

### Task: Record Daily Usage

**Scenario**: You used 3 kg of rice for lunch

1. Go to **"Stock Movements"**
2. Click **"Record Movement"**
3. Select **"Rice"** from dropdown
4. Choose **"Usage"**
5. Enter **"3"** as quantity
6. Add note: **"Lunch preparation"**
7. Click **"Save"**
8. ✅ Rice stock reduced by 3 kg

---

### Task: Request Urgent Item

**Scenario**: Sugar is finished, need 25 kg urgently

1. Go to **"Purchase Requests"**
2. Click **"Request Item"**
3. Select **"Sugar"**
4. Enter **"25"** kg
5. Enter cost estimate: **"KSh 5,000"**
6. Add note: **"URGENT - Completely out of stock"**
7. Click **"Submit"**
8. ✅ Admin notified immediately

---

### Task: Receive Delivery

**Scenario**: Delivered 50 kg of flour

1. Go to **"Stock Movements"**
2. Click **"Record Movement"**
3. Select **"Flour"** from dropdown
4. Choose **"Receipt"**
5. Enter **"50"** as quantity
6. Add note: **"Supplier: ABC Millers"**
7. Click **"Save"**
8. ✅ Flour stock increased by 50 kg

---

### Task: Bulk Approve Requests (Admin)

**Scenario**: 5 purchase requests pending, all valid

1. Go to **"Purchase Requests"**
2. **Select** all 5 requests (checkboxes)
3. Click **"Approve Selected"**
4. Enter **who received the money**
5. Click **"Confirm"**
6. ✅ All 5 approved at once!

---

## 💡 Tips & Best Practices

### ✅ DO's

- ✓ **Record movements immediately** after using items
- ✓ **Check stock levels daily** (first thing in the morning)
- ✓ **Request items early** (before they run out)
- ✓ **Add clear notes** to movements and requests
- ✓ **Keep minimum levels realistic** (not too high or low)
- ✓ **Review reports weekly** to understand usage patterns
- ✓ **Approve requests promptly** (admins)

### ❌ DON'Ts

- ✗ **Don't forget to record usage** (causes wrong stock counts)
- ✗ **Don't request excessive quantities** (money waste)
- ✗ **Don't delay approval** (causes stock-outs)
- ✗ **Don't ignore low stock alerts** (red warnings)
- ✗ **Don't delete items** unless absolutely necessary
- ✗ **Don't share your password** with anyone

---

## 🎯 Quick Reference: Dashboard Meaning

### Cards Explained

```
┌─────────────────────┐
│ TOTAL ITEMS: 18     │  ← How many different items in inventory
│ In inventory        │
└─────────────────────┘

┌─────────────────────┐
│ URGENT REORDERS: 2  │  ← Items below minimum level (ACTION NEEDED!)
│ ! Need restocking   │
└─────────────────────┘

┌─────────────────────┐
│ PENDING APPROVALS: 3│  ← Purchase requests waiting (ADMIN: REVIEW!)
│ Awaiting action     │
└─────────────────────┘

┌─────────────────────┐
│ STOCK VALUE         │  ← Total value of all items in stock
│ KSh 60,660.00       │
└─────────────────────┘
```

---

## 🔧 Troubleshooting

### Problem: Can't See "Add Item" Button

**Solution**: You're not an admin. Ask your manager to:
- Make you an admin, OR
- Ask them to add the item for you

---

### Problem: Item Not in Dropdown

**Solution**: 
1. Go to "Inventory"
2. Check if item exists
3. If not, ask admin to add it
4. If yes, refresh the page (F5)

---

### Problem: Wrong Stock Count

**Solution**:
1. Go to "Inventory"
2. Find the item
3. Click "Edit"
4. Update "Current Stock" to correct value
5. Click "Save"
6. Add a note in "Stock Movements" explaining the adjustment

---

### Problem: Request Stuck in Pending

**Solution**: 
- **For Staff**: Wait for admin approval (be patient)
- **For Admin**: Go to "Purchase Requests" → "Pending" and review it

---

### Problem: Forgot Password

**Solution**:
1. Contact your system administrator
2. They can reset your password
3. Never share passwords with others

---

## 📊 Understanding Status Colors

### Purchase Request Status

| Color | Status | Meaning |
|-------|--------|---------|
| 🟡 **Yellow** | Pending | Waiting for admin approval |
| 🔵 **Blue** | Approved | Money released, buy the item |
| 🟠 **Orange** | Awaiting Delivery | Item purchased, not yet received |
| 🟢 **Green** | Delivered | Item received and stock updated |
| 🔴 **Red** | Rejected | Not approved, see reason |

### Stock Levels

| Indicator | Meaning | Action |
|-----------|---------|--------|
| 🟢 **Green** | Stock OK | No action needed |
| 🟡 **Yellow** | Getting low | Plan to request soon |
| 🔴 **Red** | Critical | Request immediately |

---

## 📱 Mobile Usage

The system works on phones too!

**Tips for Mobile:**
- Use **portrait mode** for forms
- Use **landscape mode** for tables
- **Tap** instead of click
- **Swipe** to scroll long lists
- **Pinch** to zoom on reports

---

## 🎓 Training Recommendations

### For New Staff (Day 1)

Learn these in order:
1. ✅ How to login
2. ✅ How to view inventory
3. ✅ How to record usage
4. ✅ How to create purchase request

### For New Admins (Day 1)

Learn these in order:
1. ✅ Everything in Staff training
2. ✅ How to add new items
3. ✅ How to approve requests
4. ✅ How to generate reports
5. ✅ How to manage users

---

## 📞 Support

**Need Help?**

1. **Check this guide** first
2. **Ask your team leader**
3. **Contact IT support** at BITZ IT Consulting LTD
4. **Email**: support@bitz.co.ke (example - replace with actual)

---

## 🎉 You're Ready!

Congratulations! You now know how to use the BITZ Kitchen Inventory System.

**Remember:**
- 🎯 **Keep stock updated** daily
- 📊 **Check reports** weekly  
- 💬 **Communicate** with your team
- 🔄 **Follow the workflows** above

**Happy Managing! 🍽️**

---

*© 2025 BITZ IT Consulting LTD - Kitchen Inventory Management System*  
*Version 1.0 - Production Release*

