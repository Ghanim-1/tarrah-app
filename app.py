import os
import json
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import shutil
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import csv
from sqlalchemy import func
import qrcode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tarrah-business-secret-key-2024'

# Create instance directory first
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Set database path
db_path = os.path.join(instance_path, 'tarrah.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['BACKUP_FOLDER'] = 'backups'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['BACKUP_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(200), default='طرّة')
    currency = db.Column(db.String(10), default='OMR')
    theme = db.Column(db.String(20), default='light')
    logo = db.Column(db.String(255))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # قلم كاري or خياطة اليد
    quantity = db.Column(db.Integer, default=1, nullable=False)  # Stock quantity
    purchase_price = db.Column(db.Float, nullable=False)
    expected_selling_price = db.Column(db.Float)
    actual_selling_price = db.Column(db.Float)
    purchase_date = db.Column(db.Date, nullable=False)
    sale_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Available')  # Available, Reserved, Sold
    customer_name = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profit = db.Column(db.Float, default=0)
    images = db.relationship('ItemImage', backref='item', lazy=True, cascade='all, delete-orphan')

    def calculate_profit(self):
        if self.actual_selling_price and self.purchase_price:
            self.profit = self.actual_selling_price - self.purchase_price
        else:
            self.profit = 0
        return self.profit
    
    def get_first_image(self):
        """Get first image path for display"""
        if self.images:
            img_path = self.images[0].image_path
            # Return web-accessible path
            return f"/uploads/{os.path.basename(img_path)}"
        return None

class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    selling_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.Date, nullable=False)
    customer_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(100), nullable=False)  # Wrapping, Edge Shortening, Half Cutting
    customer_name = db.Column(db.String(200))
    price_charged = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, default=0)
    profit = db.Column(db.Float, default=0)
    service_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_profit(self):
        self.profit = self.price_charged - (self.cost or 0)
        return self.profit

class Backup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    size = db.Column(db.Float)

# ==================== AUTHENTICATION ====================

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/check-auth')
def check_auth():
    return jsonify({'authenticated': 'user_id' in session})

# ==================== DASHBOARD ====================

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
@login_required
def dashboard_data():
    total_items = Item.query.count()
    available_items = Item.query.filter_by(status='Available').count()
    sold_items = Item.query.filter_by(status='Sold').count()
    reserved_items = Item.query.filter_by(status='Reserved').count()
    
    total_purchase_cost = db.session.query(func.sum(Item.purchase_price)).scalar() or 0
    total_sales_revenue = db.session.query(func.sum(Item.actual_selling_price)).filter(Item.status=='Sold').scalar() or 0
    inventory_profit = db.session.query(func.sum(Item.profit)).filter(Item.status=='Sold').scalar() or 0
    
    services_revenue = db.session.query(func.sum(Service.price_charged)).scalar() or 0
    services_profit = db.session.query(func.sum(Service.profit)).scalar() or 0
    
    total_profit = (inventory_profit or 0) + (services_profit or 0)
    
    # Recent sales
    recent_sales = Item.query.filter_by(status='Sold').order_by(Item.sale_date.desc()).limit(5).all()
    
    # Recent services
    recent_services = Service.query.order_by(Service.service_date.desc()).limit(5).all()
    
    # Monthly data for chart
    months = []
    monthly_profits = []
    monthly_revenue = []
    
    for i in range(12, -1, -1):
        date = datetime.utcnow() - timedelta(days=30*i)
        start_date = date.replace(day=1)
        if date.month == 12:
            end_date = start_date.replace(year=date.year+1, month=1) - timedelta(days=1)
        else:
            end_date = start_date.replace(month=date.month+1) - timedelta(days=1)
        
        month_profit = db.session.query(func.sum(Item.profit)).filter(
            Item.sale_date >= start_date.date(),
            Item.sale_date <= end_date.date(),
            Item.status == 'Sold'
        ).scalar() or 0
        
        service_profit = db.session.query(func.sum(Service.profit)).filter(
            Service.service_date >= start_date.date(),
            Service.service_date <= end_date.date()
        ).scalar() or 0
        
        month_revenue = db.session.query(func.sum(Item.actual_selling_price)).filter(
            Item.sale_date >= start_date.date(),
            Item.sale_date <= end_date.date(),
            Item.status == 'Sold'
        ).scalar() or 0
        
        service_revenue = db.session.query(func.sum(Service.price_charged)).filter(
            Service.service_date >= start_date.date(),
            Service.service_date <= end_date.date()
        ).scalar() or 0
        
        months.append(start_date.strftime('%b'))
        monthly_profits.append(float(month_profit + service_profit))
        monthly_revenue.append(float(month_revenue + service_revenue))
    
    return jsonify({
        'total_items': total_items,
        'available_items': available_items,
        'sold_items': sold_items,
        'reserved_items': reserved_items,
        'total_purchase_cost': float(total_purchase_cost),
        'total_sales_revenue': float(total_sales_revenue),
        'inventory_profit': float(inventory_profit),
        'services_revenue': float(services_revenue),
        'services_profit': float(services_profit),
        'total_profit': float(total_profit),
        'recent_sales': [{
            'id': s.id,
            'name': s.name,
            'selling_price': s.actual_selling_price,
            'profit': s.profit,
            'customer': s.customer_name,
            'date': s.sale_date.isoformat()
        } for s in recent_sales],
        'recent_services': [{
            'id': s.id,
            'type': s.service_type,
            'price': s.price_charged,
            'profit': s.profit,
            'customer': s.customer_name,
            'date': s.service_date.isoformat()
        } for s in recent_services],
        'months': months,
        'monthly_profits': monthly_profits,
        'monthly_revenue': monthly_revenue,
        'service_types': {
            'wrapping': db.session.query(func.sum(Service.profit)).filter(Service.service_type=='تمصير').scalar() or 0,
            'shortening': db.session.query(func.sum(Service.profit)).filter(Service.service_type=='تقصير المصر من الأطراف').scalar() or 0,
            'cutting': db.session.query(func.sum(Service.profit)).filter(Service.service_type=='قص المصر من النصف').scalar() or 0,
        }
    })

# ==================== INVENTORY MANAGEMENT ====================

@app.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html')

@app.route('/api/items', methods=['GET', 'POST'])
@login_required
def items_api():
    if request.method == 'POST':
        data = request.get_json(silent=True) if request.is_json else request.form.to_dict()
        data = data or {}

        try:
            category = (data.get('category') or '').strip()
            purchase_price_raw = data.get('purchase_price')

            if not category:
                return jsonify({'error': 'Category is required'}), 400
            if purchase_price_raw in (None, ''):
                return jsonify({'error': 'Purchase price is required'}), 400

            # The add-product form only asks for category, price, quantity, and notes.
            # Generate safe defaults for required database fields when they are not supplied.
            code = (data.get('code') or '').strip()
            if not code:
                code = f"TRH-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

            name = (data.get('name') or '').strip() or category
            purchase_date_raw = data.get('purchase_date')
            purchase_date = (
                datetime.strptime(purchase_date_raw, '%Y-%m-%d').date()
                if purchase_date_raw else datetime.utcnow().date()
            )

            item = Item(
                code=code,
                name=name,
                category=category,
                quantity=int(data.get('quantity') or 1),
                purchase_price=float(purchase_price_raw),
                expected_selling_price=float(data.get('expected_selling_price')) if data.get('expected_selling_price') else None,
                purchase_date=purchase_date,
                status=data.get('status') or 'Available',
                notes=data.get('notes')
            )

            db.session.add(item)
            db.session.commit()
            return jsonify({'id': item.id, 'message': 'Item added successfully'})

        except ValueError as exc:
            db.session.rollback()
            return jsonify({'error': f'Invalid product data: {exc}'}), 400
        except Exception as exc:
            db.session.rollback()
            return jsonify({'error': f'Could not add item: {exc}'}), 500

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    status = request.args.get('status', '')

    query = Item.query
    if search:
        query = query.filter(
            (Item.name.ilike(f'%{search}%')) |
            (Item.code.ilike(f'%{search}%')) |
            (Item.category.ilike(f'%{search}%')) |
            (Item.notes.ilike(f'%{search}%'))
        )
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)

    items = query.order_by(Item.created_at.desc()).paginate(page=page, per_page=10, error_out=False)

    return jsonify({
        'items': [{
            'id': i.id,
            'code': i.code,
            'name': i.name,
            'category': i.category,
            'quantity': i.quantity,
            'image': i.get_first_image(),
            'purchase_price': i.purchase_price,
            'expected_selling_price': i.expected_selling_price,
            'actual_selling_price': i.actual_selling_price,
            'status': i.status,
            'customer_name': i.customer_name,
            'purchase_date': i.purchase_date.isoformat(),
            'sale_date': i.sale_date.isoformat() if i.sale_date else None,
            'profit': i.profit,
            'notes': i.notes
        } for i in items.items],
        'total': items.total,
        'pages': items.pages,
        'current_page': page
    })

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'GET':
        images = ItemImage.query.filter_by(item_id=item_id).all()
        return jsonify({
            'id': item.id,
            'code': item.code,
            'name': item.name,
            'category': item.category,
            'quantity': item.quantity,
            'purchase_price': item.purchase_price,
            'expected_selling_price': item.expected_selling_price,
            'actual_selling_price': item.actual_selling_price,
            'purchase_date': item.purchase_date.isoformat(),
            'sale_date': item.sale_date.isoformat() if item.sale_date else None,
            'status': item.status,
            'customer_name': item.customer_name,
            'profit': item.profit,
            'notes': item.notes,
            'images': [{'id': img.id, 'path': img.image_path} for img in images]
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        item.name = data.get('name', item.name)
        item.category = data.get('category', item.category)
        item.quantity = int(data.get('quantity', item.quantity) or 1)
        item.purchase_price = float(data.get('purchase_price', item.purchase_price))
        item.expected_selling_price = float(data.get('expected_selling_price')) if data.get('expected_selling_price') else None
        item.notes = data.get('notes', item.notes)
        
        if 'status' in data:
            item.status = data['status']
        if 'customer_name' in data:
            item.customer_name = data['customer_name']
        
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'})
    
    elif request.method == 'DELETE':
        # Delete images
        images = ItemImage.query.filter_by(item_id=item_id).all()
        for img in images:
            try:
                os.remove(img.image_path)
            except:
                pass
            db.session.delete(img)
        
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})

@app.route('/api/items/<int:item_id>/mark-sold', methods=['POST'])
@login_required
def mark_sold(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    
    item.status = 'Sold'
    item.actual_selling_price = float(data.get('selling_price'))
    item.sale_date = datetime.strptime(data.get('sale_date'), '%Y-%m-%d').date()
    item.customer_name = data.get('customer_name')
    item.calculate_profit()
    
    db.session.commit()
    
    return jsonify({'message': 'Item marked as sold', 'profit': item.profit})

@app.route('/api/items/<int:item_id>/images', methods=['POST'])
@login_required
def upload_image(item_id):
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Create uploads folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Generate filename with timestamp
    ext = os.path.splitext(file.filename)[1]
    filename = f"{item_id}_{int(datetime.utcnow().timestamp())}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Save image
    file.save(filepath)
    
    # Save to database
    image_obj = ItemImage(item_id=item_id, image_path=filepath)
    db.session.add(image_obj)
    db.session.commit()
    
    # Return web-accessible path
    return jsonify({
        'id': image_obj.id, 
        'path': f"/uploads/{filename}",
        'success': True
    })

@app.route('/api/items/<int:item_id>/images/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(item_id, image_id):
    img = ItemImage.query.get_or_404(image_id)
    try:
        os.remove(img.image_path)
    except:
        pass
    db.session.delete(img)
    db.session.commit()
    return jsonify({'message': 'Image deleted'})

# ==================== SALES MANAGEMENT ====================

@app.route('/sales')
@login_required
def sales():
    return render_template('sales.html')

@app.route('/api/sales', methods=['GET', 'POST'])
@login_required
def sales_api():
    if request.method == 'POST':
        data = request.get_json()
        # Sales are created through mark-sold endpoint
        return jsonify({'message': 'Use mark-sold endpoint'})
    
    page = request.args.get('page', 1, type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = Item.query.filter_by(status='Sold')
    
    if date_from:
        query = query.filter(Item.sale_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        query = query.filter(Item.sale_date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    sales_items = query.order_by(Item.sale_date.desc()).paginate(page=page, per_page=20)
    
    return jsonify({
        'sales': [{
            'id': i.id,
            'name': i.name,
            'purchase_price': i.purchase_price,
            'selling_price': i.actual_selling_price,
            'profit': i.profit,
            'customer': i.customer_name,
            'sale_date': i.sale_date.isoformat()
        } for i in sales_items.items],
        'total': sales_items.total,
        'pages': sales_items.pages
    })

# ==================== SERVICES MANAGEMENT ====================

@app.route('/services')
@login_required
def services():
    return render_template('services.html')

@app.route('/api/services', methods=['GET', 'POST'])
@login_required
def services_api():
    if request.method == 'POST':
        data = request.get_json()
        
        service = Service(
            service_type=data.get('service_type'),
            customer_name=data.get('customer_name'),
            price_charged=float(data.get('price_charged')),
            cost=float(data.get('cost', 0)),
            service_date=datetime.strptime(data.get('service_date'), '%Y-%m-%d').date(),
            notes=data.get('notes')
        )
        service.calculate_profit()
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({'id': service.id, 'message': 'Service added successfully'})
    
    page = request.args.get('page', 1, type=int)
    service_type = request.args.get('type')
    
    query = Service.query
    if service_type:
        query = query.filter_by(service_type=service_type)
    
    services_list = query.order_by(Service.service_date.desc()).paginate(page=page, per_page=20)
    
    return jsonify({
        'services': [{
            'id': s.id,
            'type': s.service_type,
            'customer': s.customer_name,
            'price': s.price_charged,
            'cost': s.cost,
            'profit': s.profit,
            'date': s.service_date.isoformat(),
            'notes': s.notes
        } for s in services_list.items],
        'total': services_list.total,
        'pages': services_list.pages
    })

@app.route('/api/services/<int:service_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': service.id,
            'type': service.service_type,
            'customer': service.customer_name,
            'price': service.price_charged,
            'cost': service.cost,
            'profit': service.profit,
            'date': service.service_date.isoformat(),
            'notes': service.notes
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        service.service_type = data.get('service_type', service.service_type)
        service.customer_name = data.get('customer_name', service.customer_name)
        service.price_charged = float(data.get('price_charged', service.price_charged))
        service.cost = float(data.get('cost', service.cost or 0))
        service.notes = data.get('notes', service.notes)
        service.calculate_profit()
        db.session.commit()
        return jsonify({'message': 'Service updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'})

# ==================== REPORTS ====================

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/api/reports/generate', methods=['POST'])
@login_required
def generate_report():
    data = request.get_json()
    period = data.get('period')
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    
    if period == 'daily':
        target_date = datetime.utcnow().date()
    elif period == 'weekly':
        target_date = datetime.utcnow().date()
        date_from = (target_date - timedelta(days=7)).isoformat()
        date_to = target_date.isoformat()
    elif period == 'monthly':
        target_date = datetime.utcnow().date()
        date_from = target_date.replace(day=1).isoformat()
        if target_date.month == 12:
            date_to = target_date.replace(year=target_date.year+1, month=1, day=1) - timedelta(days=1)
        else:
            date_to = target_date.replace(month=target_date.month+1, day=1) - timedelta(days=1)
        date_to = date_to.isoformat()
    elif period == 'yearly':
        target_date = datetime.utcnow().date()
        date_from = target_date.replace(month=1, day=1).isoformat()
        date_to = target_date.replace(month=12, day=31).isoformat()
    
    date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
    date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    
    # Get sales data
    sales = Item.query.filter(
        Item.status == 'Sold',
        Item.sale_date >= date_from,
        Item.sale_date <= date_to
    ).all()
    
    # Get services data
    services_list = Service.query.filter(
        Service.service_date >= date_from,
        Service.service_date <= date_to
    ).all()
    
    total_revenue = sum(s.actual_selling_price for s in sales) + sum(s.price_charged for s in services_list)
    total_cost = sum(s.purchase_price for s in sales) + sum(s.cost for s in services_list)
    total_profit = sum(s.profit for s in sales) + sum(s.profit for s in services_list)
    
    return jsonify({
        'period': f"{date_from} to {date_to}",
        'total_revenue': float(total_revenue),
        'total_cost': float(total_cost),
        'total_profit': float(total_profit),
        'items_sold': len(sales),
        'services_completed': len(services_list),
        'sales': [{
            'name': s.name,
            'price': s.actual_selling_price,
            'cost': s.purchase_price,
            'profit': s.profit,
            'date': s.sale_date.isoformat()
        } for s in sales],
        'services': [{
            'type': s.service_type,
            'price': s.price_charged,
            'cost': s.cost,
            'profit': s.profit,
            'date': s.service_date.isoformat()
        } for s in services_list]
    })

@app.route('/api/reports/export/<format>', methods=['POST'])
@login_required
def export_report(format):
    data = request.get_json()
    
    if format == 'pdf':
        # Create PDF
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1
        )
        elements.append(Paragraph("تقرير طرّة", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Report data
        elements.append(Paragraph(f"الفترة: {data['period']}", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        report_data = [
            ['الإجمالي', 'القيمة'],
            ['الإيرادات', f"{data['total_revenue']:.2f} OMR"],
            ['التكاليف', f"{data['total_cost']:.2f} OMR"],
            ['الربح', f"{data['total_profit']:.2f} OMR"],
            ['عدد المبيعات', str(data['items_sold'])],
            ['الخدمات المنجزة', str(data['services_completed'])]
        ]
        
        table = Table(report_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d4af37')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name='report.pdf')
    
    elif format == 'csv':
        # Create CSV
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        
        writer.writerow(['طرّة - تقرير', data['period']])
        writer.writerow([])
        writer.writerow(['الملخص', ''])
        writer.writerow(['الإيرادات', f"{data['total_revenue']:.2f}"])
        writer.writerow(['التكاليف', f"{data['total_cost']:.2f}"])
        writer.writerow(['الربح', f"{data['total_profit']:.2f}"])
        writer.writerow([])
        writer.writerow(['المبيعات'])
        writer.writerow(['الاسم', 'السعر', 'التكلفة', 'الربح', 'التاريخ'])
        
        for sale in data['sales']:
            writer.writerow([sale['name'], sale['price'], sale['cost'], sale['profit'], sale['date']])
        
        csv_buffer.seek(0)
        return send_file(
            io.BytesIO(csv_buffer.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='report.csv'
        )

# ==================== SETTINGS ====================

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/api/settings', methods=['GET', 'PUT'])
@login_required
def settings_api():
    settings_obj = Settings.query.first()
    if not settings_obj:
        settings_obj = Settings()
        db.session.add(settings_obj)
        db.session.commit()
    
    if request.method == 'GET':
        return jsonify({
            'business_name': settings_obj.business_name,
            'currency': settings_obj.currency,
            'theme': settings_obj.theme,
            'logo': settings_obj.logo
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        settings_obj.business_name = data.get('business_name', settings_obj.business_name)
        settings_obj.currency = data.get('currency', settings_obj.currency)
        settings_obj.theme = data.get('theme', settings_obj.theme)
        db.session.commit()
        return jsonify({'message': 'Settings updated'})

@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    user = User.query.get(session['user_id'])
    
    if not check_password_hash(user.password, data.get('old_password')):
        return jsonify({'error': 'Incorrect password'}), 401
    
    user.password = generate_password_hash(data.get('new_password'))
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'})

# ==================== BACKUP & RESTORE ====================

@app.route('/api/backup', methods=['POST'])
@login_required
def backup_data():
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Backup database
    db_backup = f"tarrah_backup_{timestamp}.db"
    db_backup_path = os.path.join(app.config['BACKUP_FOLDER'], db_backup)
    shutil.copy('instance/tarrah.db', db_backup_path)
    
    # Backup uploads
    uploads_backup = f"uploads_backup_{timestamp}.zip"
    uploads_backup_path = os.path.join(app.config['BACKUP_FOLDER'], uploads_backup)
    shutil.make_archive(uploads_backup_path.replace('.zip', ''), 'zip', app.config['UPLOAD_FOLDER'])
    
    backup_obj = Backup(filename=db_backup, size=os.path.getsize(db_backup_path))
    db.session.add(backup_obj)
    db.session.commit()
    
    return jsonify({'message': 'Backup created successfully', 'filename': db_backup})

@app.route('/api/backups', methods=['GET'])
@login_required
def list_backups():
    backups = Backup.query.order_by(Backup.created_at.desc()).all()
    return jsonify([{
        'id': b.id,
        'filename': b.filename,
        'created_at': b.created_at.isoformat(),
        'size': b.size
    } for b in backups])

@app.route('/api/restore/<int:backup_id>', methods=['POST'])
@login_required
def restore_backup(backup_id):
    backup = Backup.query.get_or_404(backup_id)
    backup_path = os.path.join(app.config['BACKUP_FOLDER'], backup.filename)
    
    if os.path.exists(backup_path):
        shutil.copy(backup_path, 'instance/tarrah.db')
        return jsonify({'message': 'Backup restored successfully'})
    
    return jsonify({'error': 'Backup file not found'}), 404

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ==================== INITIALIZATION ====================

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password=generate_password_hash('admin123'))
            db.session.add(admin)
            
            # Create default settings
            settings_obj = Settings(business_name='طرّة', currency='OMR', theme='light')
            db.session.add(settings_obj)
            
            db.session.commit()
            print("✓ Default admin user created: username=admin, password=admin123")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
