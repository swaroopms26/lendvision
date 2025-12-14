"""
Debug script to check if user data is properly linked to loan applications
"""
from app import create_app, db
from app.models import LoanApplication, User

app = create_app()

with app.app_context():
    # Get the first loan application
    app_to_check = LoanApplication.query.first()
    
    if app_to_check:
        print(f"Application ID: {app_to_check.id}")
        print(f"User ID in application: {app_to_check.user_id}")
        print(f"User object: {app_to_check.user}")
        
        if app_to_check.user:
            print(f"User name: {app_to_check.user.name}")
            print(f"User email: {app_to_check.user.email}")
        else:
            print("WARNING: User object is None!")
            # Try to load manually
            user = User.query.get(app_to_check.user_id)
            if user:
                print(f"User found separately: {user.name} ({user.email})")
            else:
                print("ERROR: No user found with that ID!")
    else:
        print("No loan applications in database")
