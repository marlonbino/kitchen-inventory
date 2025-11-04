# 🚀 Deployment Checklist

## Pre-Deployment Status ✅

- ✅ **Code Committed**: All changes pushed to GitHub (both repositories)
- ✅ **User Guide**: Comprehensive documentation created with workflow diagrams
- ✅ **Database Cleaned**: Test data removed, categories and users preserved
- ✅ **UI Enhanced**: Animations, icons, and responsive design complete
- ✅ **Features Complete**: All requisition workflows implemented
- ✅ **Reports Ready**: Analytics with purchase history functional
- ✅ **Migrations Ready**: All database migrations prepared

---

## 📋 Deployment Steps

### 1. Server Setup

**Backend Requirements:**
- [ ] Python 3.9+ installed
- [ ] pip package manager
- [ ] Virtual environment support
- [ ] PostgreSQL or MySQL database (production)
- [ ] Web server (Gunicorn/uWSGI)
- [ ] Nginx (reverse proxy)

**Frontend Requirements:**
- [ ] Node.js 16+ and npm
- [ ] Build tool (Vite)
- [ ] Static file hosting

---

### 2. Backend Deployment

```bash
# 1. Clone repository
git clone https://github.com/BITZ-IT-Consulting-LTD/inventory-system.git
cd inventory-system/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp env.example .env
nano .env  # Edit with production settings
```

**Update `.env` for production:**
```env
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

```bash
# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Test the server
python manage.py runserver
# Visit http://localhost:8000/api/ to verify
```

---

### 3. Frontend Deployment

```bash
# 1. Navigate to frontend
cd ../frontend

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with production API URL
```

**Update `.env` for production:**
```env
VITE_API_BASE_URL=https://api.your-domain.com/api
```

```bash
# 4. Build for production
npm run build

# 5. Test the build locally (optional)
npm run preview

# 6. Deploy dist/ folder to hosting
# Upload dist/ contents to your web server
```

---

### 4. Database Setup (Production)

**Option A: Start Fresh (Recommended)**
```bash
# Database will be empty except for migrations
python manage.py migrate
python manage.py createsuperuser
```

**Option B: Import Existing Data (With Categories)**
```bash
# If you have a database backup with categories
python manage.py migrate
python manage.py loaddata backup.json  # If you have fixtures
```

---

### 5. Web Server Configuration

**Nginx Configuration (example):**
```nginx
# Backend API
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/backend/staticfiles/;
    }
}

# Frontend
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

**Run Backend with Gunicorn:**
```bash
gunicorn kitchen_inventory.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

### 6. SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
sudo certbot --nginx -d api.your-domain.com

# Auto-renewal is configured automatically
```

---

### 7. Initial Data Setup

1. **Login as superuser**: Visit your domain
2. **Create Categories**:
   - Groceries
   - Meat
   - Dairy
   - Produce
   - Beverages
   - Spices
   - Breakfast
   - Cereals
   - Drinks
   
3. **Add Initial Items**: Add items under appropriate categories

4. **Create Staff Users**:
   - Go to Admin Panel → Users
   - Create accounts for kitchen staff
   - Assign appropriate permissions

---

### 8. Post-Deployment Verification

- [ ] **Backend API**: Test `/api/` endpoint
- [ ] **Frontend**: Homepage loads correctly
- [ ] **Login**: Can authenticate users
- [ ] **Add Item**: Can create new inventory item
- [ ] **Stock Movement**: Can record usage/receipt
- [ ] **Purchase Request**: Can create and approve requests
- [ ] **Reports**: Analytics and printing work
- [ ] **Mobile**: Test on mobile devices
- [ ] **SSL**: HTTPS working correctly

---

### 9. Monitoring & Maintenance

**Setup Monitoring:**
- [ ] Application logs (Django + Nginx)
- [ ] Error tracking (Sentry recommended)
- [ ] Uptime monitoring
- [ ] Database backups (daily recommended)

**Backup Strategy:**
```bash
# Database backup
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Or PostgreSQL backup
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

---

### 10. Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY generated
- [ ] ALLOWED_HOSTS configured correctly
- [ ] CORS_ALLOWED_ORIGINS restricted to your domain
- [ ] Firewall configured (only 80, 443 open)
- [ ] Database password is strong
- [ ] Regular security updates
- [ ] HTTPS enforced

---

## 🆘 Troubleshooting

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` and check Nginx static file path

### Issue: CORS errors
**Solution**: Update `CORS_ALLOWED_ORIGINS` in backend settings with frontend URL

### Issue: Database connection error
**Solution**: Check `DATABASE_URL` in `.env` file, verify database is running

### Issue: 502 Bad Gateway
**Solution**: Check if Gunicorn is running, verify Nginx proxy_pass configuration

---

## 📞 Support Contacts

- **Technical Issues**: IT Department
- **User Training**: Refer to USER_GUIDE.md
- **System Admin**: [Your Contact]

---

## 🎉 Deployment Complete!

Once all checkboxes are ticked, your system is live and ready for use!

**Repository Links:**
- **User Repo**: https://github.com/marlonbino/kitchen-inventory
- **BITZ Repo**: https://github.com/BITZ-IT-Consulting-LTD/inventory-system

**Last Updated**: November 4, 2025
**Version**: 1.0.0 (Production Ready)

---

*© 2025 BITZ IT Consulting LTD - Kitchen Inventory Management System*

