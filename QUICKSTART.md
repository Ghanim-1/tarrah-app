# طرّة - Quick Start Guide (دليل البدء السريع)

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

You should see:
```
✓ Default admin user created: username=admin, password=admin123
 * Running on http://0.0.0.0:5000
```

### Step 3: Open in Browser
- **Laptop:** Go to `http://localhost:5000`
- **Phone (same WiFi):** Go to `http://<YOUR-IP>:5000`

---

## 📱 Finding Your IP Address for Mobile Access

### Windows:
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

### Mac/Linux:
```bash
ifconfig
# or
hostname -I
```

---

## 🔑 Login Credentials

| Field | Value |
|-------|-------|
| Username | admin |
| Password | admin123 |

⚠️ **Change password immediately after first login!**

---

## 📦 What's Included

✅ Complete inventory management system
✅ Sales and profit tracking
✅ Service management (3 service types)
✅ Professional dashboard with charts
✅ Report generation (PDF/CSV export)
✅ Backup and restore functionality
✅ Arabic and English interface
✅ Mobile-responsive design
✅ Dark/Light theme toggle
✅ Local storage (no cloud needed)

---

## 🎯 First Time Tasks

1. **Change Admin Password**
   - Go to الإعدادات (Settings)
   - Click الأمان (Security)
   - Enter current password and new password
   - Save

2. **Add Your First Product**
   - Go to المخزون (Inventory)
   - Click "+ إضافة منتج جديد" (Add New Product)
   - Fill in product details
   - Save

3. **Record a Sale**
   - Find product in Inventory
   - Click "بيع" (Sell)
   - Enter selling price and date
   - Save

4. **Create a Backup**
   - Go to الإعدادات (Settings)
   - Scroll to النسخ الاحتياطية (Backups)
   - Click "📦 إنشاء نسخة احتياطية"

---

## 🎨 User Interface Overview

| Page | Purpose | Arabic Name |
|------|---------|-------------|
| Dashboard | Business overview & charts | لوحة التحكم |
| Inventory | Manage products | إدارة المخزون |
| Sales | Track sales transactions | المبيعات |
| Services | Record services | الخدمات |
| Reports | Generate reports | التقارير |
| Settings | Configure system | الإعدادات |

---

## 💡 Useful Shortcuts

- **Search Products:** Type in search box in Inventory
- **Filter by Status:** Select status dropdown in Inventory
- **Export Report:** Go to Reports → Generate → Export PDF/CSV
- **Dark Mode:** Go to Settings → Theme → Dark
- **View Dashboard:** Click طرّة logo anytime

---

## ❓ Common Questions

**Q: How do I access from my phone?**
A: Make sure both devices are on same WiFi. On phone, go to `http://<your-laptop-ip>:5000`

**Q: How do I backup my data?**
A: Settings → Backups → Create Backup (do this regularly!)

**Q: Can I change the username?**
A: Not in the current version. You can modify `app.py` if needed.

**Q: Is my data safe?**
A: Yes! Data is stored locally on your laptop, not on any cloud.

**Q: Can I access from the internet?**
A: Not recommended. This is designed for local network use only.

---

## 🔧 Troubleshooting

**Port already in use?**
- Edit `app.py` line: `app.run(host='0.0.0.0', port=5001, debug=True)`

**Can't connect from phone?**
- Check both devices on same WiFi
- Verify correct IP address
- Check Windows Firewall settings

**Forgot password?**
- Delete `instance/tarrah.db`
- Run `python app.py` again
- Default credentials will be restored

---

## 📊 Sample Data Entry

### Adding a Misar Product
- Code: `MSR-001-RED`
- Name: Red Omani Misar Premium
- Color: Red
- Brand: Premium Edition
- Condition: New
- Purchase Price: 150 OMR
- Expected Selling Price: 250 OMR

### Recording a Service
- Type: تمصير (Wrapping)
- Price: 25 OMR
- Cost: 5 OMR
- Customer: Ahmad Al-Balushi
- Date: Today

---

## 🎓 Learn More

Read `README.md` for:
- Detailed feature documentation
- Advanced configuration
- Security information
- Database structure
- API endpoints

---

## 🚀 You're Ready!

Congratulations! Your طرّة business management system is ready to use.

**Remember:**
1. Keep your passwords secure
2. Make regular backups
3. Use the dashboard to monitor your business

Happy managing! 🎉

---

**Version:** 1.0.0
**For:** طرّة Business Management System
