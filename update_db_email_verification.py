from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Check if columns exist to avoid errors
    conn = db.engine.connect()
    
    # Check for is_email_verified
    try:
        conn.execute(text("SELECT is_email_verified FROM user LIMIT 1"))
        print("Column 'is_email_verified' already exists.")
    except Exception:
        print("Adding column 'is_email_verified'...")
        # Default existing users to True to avoid locking them out
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN is_email_verified BOOLEAN DEFAULT 1"))
            conn.commit()

    # Check for email_verification_token
    try:
        conn.execute(text("SELECT email_verification_token FROM user LIMIT 1"))
        print("Column 'email_verification_token' already exists.")
    except Exception:
        print("Adding column 'email_verification_token'...")
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN email_verification_token VARCHAR(100)"))
            conn.commit()

    print("Database update complete.")
