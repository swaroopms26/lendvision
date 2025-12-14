from app import create_app, db
from app.models import User, Bank

app = create_app()

def seed():
    with app.app_context():
        # Clean Start
        db.drop_all()
        db.create_all()
        
        # Create Banks
        bank_a = Bank(name="Bank of Py", settings='{"ltv_threshold": 0.8, "dti_threshold": 0.55}')
        bank_b = Bank(name="Flask Financial", settings='{"ltv_threshold": 0.75, "dti_threshold": 0.50}')
        db.session.add_all([bank_a, bank_b])
        db.session.commit()
        
        # Super Admin (Global)
        if not User.query.filter_by(email='super@platform.com').first():
            super_admin = User(name='Super Admin', email='super@platform.com', role='super_admin')
            super_admin.set_password('super123')
            db.session.add(super_admin)
            print("Created Super Admin")

        # Bank A Users
        if not User.query.filter_by(email='admin@bank-a.com').first():
            admin_a = User(name='Admin Bank A', email='admin@bank-a.com', role='bank_admin', bank_id=bank_a.id)
            admin_a.set_password('admin123')
            db.session.add(admin_a)
            
            officer_a = User(name='Officer Bank A', email='officer@bank-a.com', role='officer', bank_id=bank_a.id)
            officer_a.set_password('officer123')
            db.session.add(officer_a)
            print("Created Users for Bank A")

        # Bank B Users
        if not User.query.filter_by(email='admin@bank-b.com').first():
            admin_b = User(name='Admin Bank B', email='admin@bank-b.com', role='bank_admin', bank_id=bank_b.id)
            admin_b.set_password('admin123')
            db.session.add(admin_b)
            
            officer_b = User(name='Officer Bank B', email='officer@bank-b.com', role='officer', bank_id=bank_b.id)
            officer_b.set_password('officer123')
            db.session.add(officer_b)
            print("Created Users for Bank B")
            
        # Global Customer
        if not User.query.filter_by(email='customer@gmail.com').first():
            customer = User(name='John Doe', email='customer@gmail.com', role='customer') # No bank_id
            customer.set_password('customer123')
            db.session.add(customer)
            print("Created Global Customer")
            
        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed()
