from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    conn = db.engine.connect()
    
    # Add interest_rate
    try:
        conn.execute(text("SELECT interest_rate FROM loan_application LIMIT 1"))
        print("Column 'interest_rate' already exists.")
    except Exception:
        print("Adding column 'interest_rate'...")
        with db.engine.connect() as conn:  # New connection for transaction
            conn.execute(text("ALTER TABLE loan_application ADD COLUMN interest_rate FLOAT DEFAULT 10.0"))
            conn.commit()

    # Add is_active
    try:
        conn.execute(text("SELECT is_active FROM loan_application LIMIT 1"))
        print("Column 'is_active' already exists.")
    except Exception:
        print("Adding column 'is_active'...")
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE loan_application ADD COLUMN is_active BOOLEAN DEFAULT 0"))
            conn.commit()

    # Add accepted_at
    try:
        conn.execute(text("SELECT accepted_at FROM loan_application LIMIT 1"))
        print("Column 'accepted_at' already exists.")
    except Exception:
        print("Adding column 'accepted_at'...")
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE loan_application ADD COLUMN accepted_at DATETIME"))
            conn.commit()

    # Add disbursed_at
    try:
        conn.execute(text("SELECT disbursed_at FROM loan_application LIMIT 1"))
        print("Column 'disbursed_at' already exists.")
    except Exception:
        print("Adding column 'disbursed_at'...")
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE loan_application ADD COLUMN disbursed_at DATETIME"))
            conn.commit()
            
    print("Database update complete.")
