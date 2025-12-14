"""
Update database with DigiLocker Integration fields
"""
from app import create_app, db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    
    if 'user' in inspector.get_table_names():
        print("Checking User table for DigiLocker columns...")
        
        columns = [col['name'] for col in inspector.get_columns('user')]
        
        with db.engine.connect() as conn:
            if 'digilocker_id' not in columns:
                print("Adding digilocker_id column...")
                conn.execute(text('ALTER TABLE user ADD COLUMN digilocker_id VARCHAR(100)'))
                # SQLite doesn't support adding UNIQUE constraint via ALTER TABLE easily
                # We'll rely on app-level check or recreate table if strictly needed, 
                # but for this feature, app level check in model is sufficient + index if possible
                try:
                    conn.execute(text('CREATE UNIQUE INDEX ix_user_digilocker_id ON user(digilocker_id)'))
                except Exception as e:
                    print(f"Index creation warning: {e}")
                
            if 'is_verified' not in columns:
                print("Adding is_verified column...")
                conn.execute(text('ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT 0'))
                
            conn.commit()
            
        print("User table updated successfully!")
    else:
        print("User table not found!")

    print("\nDigiLocker fields added.")
