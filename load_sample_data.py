"""
Sample data initialization script for طرّة (Tarrah)
Run this to populate the database with sample data for testing
"""

from app import app, db, Item, Service, ItemImage
from datetime import datetime, timedelta

def load_sample_data():
    """Load sample data into the database"""
    
    with app.app_context():
        # Clear existing data (optional)
        # Item.query.delete()
        # Service.query.delete()
        
        # Sample items
        sample_items = [
            Item(
                code='MSR-001-RED',
                name='Red Omani Misar Premium',
                brand='Premium Edition',
                color='Red',
                pattern='Traditional Gold Pattern',
                condition='New',
                purchase_price=150.00,
                expected_selling_price=280.00,
                purchase_date=datetime.utcnow().date() - timedelta(days=30),
                status='Available',
                notes='High quality traditional Misar with gold threading'
            ),
            Item(
                code='MSR-002-GREEN',
                name='Green Omani Misar Classic',
                brand='Classic Series',
                color='Green',
                pattern='Traditional Pattern',
                condition='New',
                purchase_price=120.00,
                expected_selling_price=220.00,
                purchase_date=datetime.utcnow().date() - timedelta(days=20),
                status='Available',
                notes='Beautiful green with classic patterns'
            ),
            Item(
                code='MSR-003-BLUE',
                name='Blue Royal Misar',
                brand='Royal Collection',
                color='Blue',
                pattern='Royal Gold Pattern',
                condition='New',
                purchase_price=180.00,
                expected_selling_price=320.00,
                purchase_date=datetime.utcnow().date() - timedelta(days=15),
                status='Reserved',
                customer_name='Ahmed Al-Mansouri',
                notes='Premium royal blue with intricate gold work'
            ),
            Item(
                code='MSR-004-WHITE',
                name='White Wedding Misar',
                brand='Wedding Collection',
                color='White',
                pattern='Elegant Pearl Pattern',
                condition='New',
                purchase_price=200.00,
                expected_selling_price=350.00,
                purchase_date=datetime.utcnow().date() - timedelta(days=10),
                status='Sold',
                actual_selling_price=350.00,
                sale_date=datetime.utcnow().date() - timedelta(days=5),
                customer_name='Mohammed Al-Khaleeli',
                notes='Perfect for weddings and special occasions'
            ),
            Item(
                code='MSR-005-MAROON',
                name='Maroon Executive Misar',
                brand='Executive Series',
                color='Maroon',
                pattern='Business Pattern',
                condition='Used',
                purchase_price=80.00,
                expected_selling_price=150.00,
                purchase_date=datetime.utcnow().date() - timedelta(days=25),
                status='Sold',
                actual_selling_price=160.00,
                sale_date=datetime.utcnow().date() - timedelta(days=3),
                customer_name='Salem Al-Busaidi',
                notes='Gently used, excellent condition'
            ),
            Item(
                code='MSR-006-GOLD',
                name='Gold Luxury Misar',
                brand='Luxury Collection',
                color='Gold',
                pattern='Intricate Gold Pattern',
                condition='New',
                purchase_price=250.00,
                expected_selling_price=420.00,
                purchase_date=datetime.utcnow().date() - timedelta(days=5),
                status='Available',
                notes='Luxury item with premium gold threading'
            ),
        ]
        
        for item in sample_items:
            if not Item.query.filter_by(code=item.code).first():
                db.session.add(item)
        
        db.session.commit()
        print(f"✓ Added {len(sample_items)} sample items")
        
        # Sample services
        sample_services = [
            Service(
                service_type='تمصير',
                customer_name='فاطمة الحارثية',
                price_charged=25.00,
                cost=5.00,
                service_date=datetime.utcnow().date() - timedelta(days=7),
                notes='Standard wrapping service'
            ),
            Service(
                service_type='تقصير المصر من الأطراف',
                customer_name='علي الشقصي',
                price_charged=15.00,
                cost=3.00,
                service_date=datetime.utcnow().date() - timedelta(days=5),
                notes='Edge shortening - standard length'
            ),
            Service(
                service_type='قص المصر من النصف',
                customer_name='خديجة الرحبية',
                price_charged=20.00,
                cost=4.00,
                service_date=datetime.utcnow().date() - timedelta(days=3),
                notes='Cutting in half - customer request'
            ),
            Service(
                service_type='تمصير',
                customer_name='حمد البريمي',
                price_charged=30.00,
                cost=6.00,
                service_date=datetime.utcnow().date() - timedelta(days=2),
                notes='Premium wrapping with special patterns'
            ),
            Service(
                service_type='تقصير المصر من الأطراف',
                customer_name='نور الدين',
                price_charged=15.00,
                cost=3.00,
                service_date=datetime.utcnow().date() - timedelta(days=1),
                notes='Standard edge shortening'
            ),
        ]
        
        for service in sample_services:
            service.calculate_profit()
            db.session.add(service)
        
        db.session.commit()
        print(f"✓ Added {len(sample_services)} sample services")
        
        print("\n✓ Sample data loaded successfully!")
        print("\nYou can now:")
        print("1. View products in Inventory")
        print("2. See sales history")
        print("3. Check services transactions")
        print("4. View reports with sample data")

if __name__ == '__main__':
    load_sample_data()
