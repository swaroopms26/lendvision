"""
Update database with Support Ticket tables
This script handles both new installations and updates to existing databases
"""
from app import create_app, db
from app.models import SupportTicket
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    
    # Check if support_ticket table exists
    if 'support_ticket' in inspector.get_table_names():
        print("Support ticket table exists, checking for bank_id column...")
        
        # Check if bank_id column exists
        columns = [col['name'] for col in inspector.get_columns('support_ticket')]
        
        if 'bank_id' not in columns:
            print("Adding bank_id column to support_ticket table...")
            # Add the bank_id column
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE support_ticket ADD COLUMN bank_id INTEGER'))
                conn.execute(text('ALTER TABLE support_ticket ADD FOREIGN KEY(bank_id) REFERENCES bank(id)'))
                conn.commit()
            print("bank_id column added successfully!")
        else:
            print("bank_id column already exists!")
    else:
        print("Creating support ticket tables...")
        db.create_all()
        print("Tables created successfully!")
    
    print("\nDatabase updated successfully!")
    print("New/Updated tables: SupportTicket, TicketMessage")
