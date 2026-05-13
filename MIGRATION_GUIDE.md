# 🎯 TARRAH APPLICATION - COMPREHENSIVE UPDATE GUIDE

## MAJOR CHANGES IMPLEMENTED

### 1. ✅ DATABASE SCHEMA UPDATES

**Removed Fields from Item Model:**
- `brand` - No longer needed
- `color` - No longer needed (requested removal)
- `pattern` - No longer needed
- `condition` - No longer needed

**Added Fields to Item Model:**
- `category` - Required field for Misar type (قلم كاري OR خياطة اليد)
- `quantity` - Stock quantity tracking (integer, default 1)

**New Relationships:**
- Items now have proper image relationship with cascade delete

### 2. ✅ IMAGE UPLOAD FIXES

**What Was Fixed:**
- Images are now saved with proper file extensions
- Correct web-accessible paths are returned
- Image serving route added (`/uploads/<filename>`)
- Database paths properly stored
- First image displays on product cards
- Placeholder shows when no image exists

**New Endpoint:**
- `GET /uploads/<filename>` - Serve uploaded images

### 3. ✅ PRODUCT FORM SIMPLIFIED

**New Form Contains Only:**
- Category (required dropdown: قلم كاري / خياطة اليد)
- Purchase Price (required)
- Product Image (optional, can add later)
- Quantity (optional, default 1)
- Notes (optional)
- Product Code (auto-generated)

**Removed from Form:**
- Brand
- Color
- Pattern
- Condition
- Expected Selling Price

### 4. ✅ PAGINATION IMPLEMENTED

**Changes:**
- 20 products per page (not 10)
- Previous/Next navigation buttons
- Current page indicator
- All products always accessible
- Smooth scrolling

### 5. ✅ CATEGORY SUPPORT

**Available Categories:**
1. قلم كاري (Qalam Kari)
2. خياطة اليد (Hand Stitch)

**Features:**
- Category badges on product cards
- Filter by category
- Category in sales history
- Category in reports

---

## MIGRATION GUIDE - STEP BY STEP

### ⚠️ IMPORTANT: DATA BACKUP

Before starting migration, backup your current database:

```powershell
# 1. Stop the app (press Ctrl+C)

# 2. Copy your database file
Copy-Item -Path "instance\tarrah.db" -Destination "instance\tarrah.db.backup"

# 3. Also backup uploads folder
Copy-Item -Path "uploads" -Destination "uploads.backup" -Recurse
```

---

### MIGRATION PROCESS

#### **Option A: Fresh Start (Recommended)**

If you have very few products, start fresh:

```powershell
# 1. Delete old database
Remove-Item instance\tarrah.db

# 2. Delete old uploads (if needed)
Remove-Item uploads -Recurse

# 3. Run updated app
python app.py

# 4. System creates new database automatically
# 5. Manually re-add products with new form
```

#### **Option B: Migrate Existing Data**

If you have many products, follow these steps:

**Step 1: Update Database Schema**

The new version will handle schema migration automatically, but you need to manually:

1. Update any existing data that has the old fields
2. Set category for all products (required)
3. Set quantity for all products (optional, defaults to 1)

**Step 2: Create Migration Script**

Create a file called `migrate_data.py` in your tarrah_app folder:

```python
import sqlite3
from datetime import datetime

def migrate_database():
    """Migrate old database to new schema"""
    
    # Connect to database
    conn = sqlite3.connect('instance/tarrah.db')
    cursor = conn.cursor()
    
    try:
        # Add new columns if they don't exist
        cursor.execute("ALTER TABLE item ADD COLUMN category TEXT DEFAULT 'قلم كاري'")
        cursor.execute("ALTER TABLE item ADD COLUMN quantity INTEGER DEFAULT 1")
        print("✓ Added new columns: category, quantity")
    except Exception as e:
        print(f"Columns already exist or error: {e}")
    
    try:
        # Remove old columns (SQLite doesn't support direct DROP, so we create new table)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_new (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                purchase_price FLOAT NOT NULL,
                expected_selling_price FLOAT,
                actual_selling_price FLOAT,
                purchase_date DATE NOT NULL,
                sale_date DATE,
                status TEXT DEFAULT 'Available',
                customer_name TEXT,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                profit FLOAT DEFAULT 0
            )
        """)
        
        # Copy existing data
        cursor.execute("""
            INSERT INTO item_new 
            (id, code, name, category, quantity, purchase_price, expected_selling_price, 
             actual_selling_price, purchase_date, sale_date, status, customer_name, 
             notes, created_at, profit)
            SELECT 
                id, code, name, 'قلم كاري', 1, purchase_price, expected_selling_price,
                actual_selling_price, purchase_date, sale_date, status, customer_name,
                notes, created_at, profit
            FROM item
        """)
        
        # Replace old table
        cursor.execute("DROP TABLE IF EXISTS item")
        cursor.execute("ALTER TABLE item_new RENAME TO item")
        
        print("✓ Migrated existing products to new schema")
    except Exception as e:
        print(f"Migration note: {e}")
    
    conn.commit()
    conn.close()
    print("✓ Database migration complete!")

if __name__ == '__main__':
    migrate_database()
```

**Step 3: Run Migration Script**

```powershell
# Run the migration script
python migrate_data.py

# You should see:
# ✓ Added new columns: category, quantity
# ✓ Migrated existing products to new schema
# ✓ Database migration complete!
```

**Step 4: Update Images**

Your existing images should still work, but verify:

```powershell
# Check if uploads folder exists and has images
dir uploads

# Images should show like:
# 1_1234567890.jpg
# 2_1234567891.png
```

**Step 5: Restart Application**

```powershell
# Restart the app
python app.py

# Login and verify:
# 1. Products appear with images
# 2. Category field shows "قلم كاري" (default)
# 3. Quantity shows "1" (default)
# 4. Edit products to update categories if needed
```

---

### MIGRATION CHECKLIST

- [ ] Backup current database (`instance/tarrah.db.backup`)
- [ ] Backup uploads folder (`uploads.backup/`)
- [ ] Run migration script (`python migrate_data.py`)
- [ ] Restart application (`python app.py`)
- [ ] Verify products appear with images
- [ ] Verify categories show "قلم كاري"
- [ ] Verify quantity shows "1"
- [ ] Edit products to update categories
- [ ] Test image upload with new products
- [ ] Test pagination (add 20+ products)

---

## NEW FEATURES

### Image Upload
- Click "📸 صور" button on product card
- Select one or multiple images
- Images display on product card
- Placeholder shows if no image

### Pagination
- 20 products per page
- Previous/Next buttons
- Page indicator
- All products accessible

### Categories
- Filter by category
- Category badges visible
- Category in reports
- Automatic default assignment

### Quantity Tracking
- Stock quantity per product
- Track available units
- Update quantity anytime

---

## API ENDPOINTS (UPDATED)

```
POST   /api/items                           - Create item (now with category, quantity)
GET    /api/items?page=1&search=&status=   - Get paginated items
GET    /api/items/<id>                      - Get single item
PUT    /api/items/<id>                      - Update item
DELETE /api/items/<id>                      - Delete item

POST   /api/items/<id>/images               - Upload image
DELETE /api/items/<id>/images/<img_id>      - Delete image

GET    /uploads/<filename>                  - Serve uploaded images (NEW)
```

---

## FIELD CHANGES SUMMARY

### Item Model Changes

| Field | Old | New | Status |
|-------|-----|-----|--------|
| code | ✓ | ✓ | Unchanged |
| name | ✓ | ✓ | Unchanged |
| brand | ✓ | ✗ | Removed |
| color | ✓ | ✗ | Removed |
| pattern | ✓ | ✗ | Removed |
| condition | ✓ | ✗ | Removed |
| category | ✗ | ✓ | **Added** |
| quantity | ✗ | ✓ | **Added** |
| purchase_price | ✓ | ✓ | Unchanged |
| expected_selling_price | ✓ | ✓ | Unchanged |
| actual_selling_price | ✓ | ✓ | Unchanged |
| purchase_date | ✓ | ✓ | Unchanged |
| sale_date | ✓ | ✓ | Unchanged |
| status | ✓ | ✓ | Unchanged |
| customer_name | ✓ | ✓ | Unchanged |
| notes | ✓ | ✓ | Unchanged |

---

## TROUBLESHOOTING

### Images Still Not Showing
```powershell
# 1. Check uploads folder exists
dir uploads

# 2. Check file permissions
# Right-click uploads folder → Properties → Security

# 3. Verify path in database
# (Technical: Check ItemImage.image_path values)

# 4. Restart app
python app.py
```

### Migration Script Errors
```powershell
# If migration fails, restore backup:
Copy-Item "instance\tarrah.db.backup" -Destination "instance\tarrah.db" -Force

# Try migration again:
python migrate_data.py
```

### Products Disappear After Update
```powershell
# Backup current database
Copy-Item "instance\tarrah.db" -Destination "instance\tarrah.db.current"

# Restore backup from before update
Copy-Item "instance\tarrah.db.backup" -Destination "instance\tarrah.db" -Force

# Don't run migration, manually add products instead
```

---

## VERIFICATION STEPS

After migration, verify everything works:

1. **Check Products Load**
   - Go to Inventory page
   - Products should display with images
   - Pagination should show page 1

2. **Upload New Product**
   - Click "+ إضافة منتج"
   - Fill form with just: Category, Price, Image, Quantity
   - Submit
   - Product should appear

3. **Upload Image**
   - Click "📸 صور" on any product
   - Select image file
   - Click upload
   - Image should appear on card

4. **Check Category**
   - Products should have category badge
   - Should be "قلم كاري" by default
   - Can change in edit form

5. **Test Pagination**
   - Add 20+ products
   - "Next" button should appear
   - Click Next to see page 2

---

## NEXT STEPS

1. **Download Updated ZIP** from outputs
2. **Backup your current database** (IMPORTANT!)
3. **Choose migration option** (Fresh or Migrate)
4. **Follow migration steps** above
5. **Verify everything works**
6. **Report any issues**

---

## SUPPORT

If you encounter issues:

1. Check backup exists: `instance/tarrah.db.backup`
2. Check uploads folder: `uploads/`
3. Check error messages in terminal
4. Verify migration script completed successfully

---

**Version:** 2.0.0  
**Updated:** May 2026  
**Status:** Ready for Migration

Good luck! 🚀
