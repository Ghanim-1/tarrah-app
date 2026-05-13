# طرّة (Tarrah) - Business Management System

A complete, professional business management system designed specifically for managing Omani traditional Misar inventory, sales, and services. Built with Flask, SQLite, and modern responsive web technologies.

## 🎯 Features

### Dashboard
- Real-time business statistics
- Monthly profit and revenue charts
- Recent sales and services overview
- Quick business health metrics

### Inventory Management (📦 المخزون)
- Add, edit, and delete Misar products
- Track product details (code, color, pattern, condition)
- Multiple image uploads per product
- Mark items as Available, Reserved, or Sold
- Quick profit calculation
- Search and filter by status, color, or code

### Sales Management (💰 المبيعات)
- Record item sales with actual selling price
- Automatic profit calculation
- Customer name tracking
- Sales date recording
- Date range filtering
- Sales summary statistics

### Services Management (🔧 الخدمات)
Three types of services supported:
- تمصير (Misar Wrapping)
- تقصير المصر من الأطراف (Edge Shortening)
- قص المصر من النصف (Half Cutting)

Features:
- Record service transactions
- Track customer information
- Calculate service profit
- Service type statistics

### Reports & Analytics (📊 التقارير)
- Generate reports by period (Daily, Weekly, Monthly, Yearly, Custom)
- Comprehensive summary statistics
- Sales and service details
- Export to PDF and CSV formats
- Printable reports

### Settings ⚙️
- Business name and currency configuration
- Light/Dark theme toggle
- Secure password management
- Backup and restore functionality

### Security
- Username and password authentication
- Hashed password storage
- Session management
- Admin-only access

## 📋 System Requirements

- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- SQLite (included with Python)
- 50MB disk space

## 🚀 Installation & Setup

### 1. Install Python Dependencies

```bash
# Navigate to the project directory
cd tarrah_app

# Install required packages
pip install -r requirements.txt
```

### 2. Initialize the Application

```bash
# Run the Flask app - it will automatically initialize the database
python app.py
```

The server will start at `http://localhost:5000`

### 3. First Login

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **Important:** Change the default password immediately after first login in Settings → Security

## 💻 How to Access from Mobile

Once the server is running on your laptop:

1. **Find your laptop's local IP address:**
   - **Windows:** Open Command Prompt and type `ipconfig`, look for "IPv4 Address"
   - **Mac/Linux:** Open Terminal and type `ifconfig` or `hostname -I`
   - Usually looks like: `192.168.x.x`

2. **On your phone (same WiFi network):**
   - Open a web browser
   - Navigate to: `http://<your-laptop-ip>:5000`
   - Example: `http://192.168.1.100:5000`

3. **Login with your credentials**

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- Desktop computers
- Tablets
- Smartphones (both iOS and Android)

## 🗂️ Project Structure

```
tarrah_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── instance/             # Database storage
│   └── tarrah.db        # SQLite database
├── templates/           # HTML templates
│   ├── login.html       # Login page
│   ├── base.html        # Base template with navigation
│   ├── dashboard.html   # Dashboard
│   ├── inventory.html   # Inventory management
│   ├── sales.html       # Sales management
│   ├── services.html    # Services management
│   ├── reports.html     # Reports
│   └── settings.html    # Settings
├── static/              # CSS and JavaScript files
├── uploads/             # Product images storage
└── backups/            # Database backups
```

## 🔧 Usage Guide

### Adding a New Product (منتج جديد)
1. Navigate to المخزون (Inventory)
2. Click "+ إضافة منتج جديد" (Add New Product)
3. Fill in the product details:
   - Unique code
   - Name/Description
   - Color
   - Purchase price
   - Purchase date
4. Click "حفظ" (Save)

### Recording a Sale (تسجيل مبيعة)
1. Go to المخزون (Inventory)
2. Find the product to sell
3. Click "بيع" (Sell) button
4. Enter:
   - Selling price
   - Sale date
   - Customer name (optional)
5. Click "تسجيل البيع" (Record Sale)

### Adding a Service (خدمة جديدة)
1. Navigate to الخدمات (Services)
2. Click "+ إضافة خدمة" (Add Service)
3. Select service type:
   - تمصير (Wrapping)
   - تقصير المصر من الأطراف (Edge Shortening)
   - قص المصر من النصف (Half Cutting)
4. Enter price and date
5. Click "حفظ" (Save)

### Generating Reports (إنشاء تقرير)
1. Go to التقارير (Reports)
2. Select report period:
   - Daily (يومي)
   - Weekly (أسبوعي)
   - Monthly (شهري)
   - Yearly (سنوي)
   - Custom date range
3. Click "إنشاء التقرير" (Generate Report)
4. Export as PDF or CSV

### Backup & Restore
1. Go to الإعدادات (Settings)
2. In "النسخ الاحتياطية" (Backups) section:
   - Click "📦 إنشاء نسخة احتياطية" to create backup
   - Click "استرجاع" to restore from backup

## 💰 Profit Calculation

**Inventory Profit:**
```
Profit = Actual Selling Price - Purchase Price
```

**Service Profit:**
```
Profit = Price Charged - Cost
```

**Overall Profit:**
```
Total Profit = Inventory Profit + Services Profit
```

## 🎨 Customization

### Changing Colors
Edit the CSS variables in `templates/base.html`:
```css
:root {
    --gold: #d4af37;      /* Primary gold color */
    --dark: #1a1a1a;      /* Dark text/background */
    --light: #f5f5f5;     /* Light background */
}
```

### Language Support
The application supports both Arabic (RTL) and English with proper right-to-left layout for Arabic content.

## 🔐 Security Notes

1. **Password Security:**
   - Passwords are hashed using Werkzeug's security functions
   - Never share your admin password
   - Change default password on first login

2. **Local Storage:**
   - Data stored locally in SQLite database
   - No cloud synchronization (by design)
   - Regular backups recommended

3. **Network Access:**
   - Only accessible from devices on the same WiFi network
   - Not exposed to the internet
   - Suitable for private business use only

## 🆘 Troubleshooting

### Port 5000 Already in Use
```bash
# Change the port in app.py
app.run(host='0.0.0.0', port=5001, debug=True)  # Use port 5001 instead
```

### Can't Connect from Mobile
1. Verify both devices are on same WiFi
2. Check firewall settings
3. Confirm correct IP address and port
4. Restart the Flask server

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
rm instance/tarrah.db
python app.py  # Will recreate database
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📊 Data Export

### CSV Export
- Contains all transaction data
- Compatible with Excel, Google Sheets
- Useful for external analysis

### PDF Export
- Professional report format
- Ready for printing
- Includes business branding

## 🎯 Tips for Best Use

1. **Regular Backups:** Create backups weekly in Settings
2. **Accurate Data Entry:** Double-check product codes and prices
3. **Customer Records:** Always record customer names for tracking
4. **Regular Reviews:** Check dashboard daily for business health
5. **Use Filters:** Use search and filters for quick data access

## 📱 Browser Compatibility

- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Performance Tips

- The app can handle thousands of products and transactions
- Backups should be done regularly
- For large datasets, use CSV export for analysis
- Database typically stays under 50MB for typical use

## 📝 License

This application is provided as-is for personal business use.

## 🤝 Support & Updates

For issues or feature requests:
1. Check the troubleshooting section
2. Review Flask and SQLAlchemy documentation
3. Ensure all dependencies are installed correctly

## 📞 Contact Information

Built with ❤️ for Omani businesses managing traditional Misar.

---

**Version:** 1.0.0  
**Last Updated:** May 2026  
**Created for:** طرّة (Tarrah) Business Management
