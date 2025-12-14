import requests
import os

def reset_db():
    # Try to delete the db file
    db_path = os.path.join('instance', 'loan.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("Database deleted.")
        except Exception as e:
            print(f"Error deleting DB: {e}")
            
    # Run seed script
    os.system('python seed_db.py')
    print("Database seeded.")

def test_features():
    session = requests.Session()
    
    # 1. Test Admin Login & Export
    print("\n--- Testing Admin Export ---")
    login_url = 'http://127.0.0.1:5001/login'
    session.post(login_url, data={'email': 'admin@bank.com', 'password': 'admin123'})
    
    resp = session.get('http://127.0.0.1:5001/admin/export')
    if resp.status_code == 200 and 'text/csv' in resp.headers.get('Content-Type', ''):
        print("PASS: Admin Export (CSV received)")
    else:
        print(f"FAIL: Admin Export. Status: {resp.status_code}, Type: {resp.headers.get('Content-Type')}")

    # 2. Test Customer Calculator
    print("\n--- Testing Customer Calculator ---")
    # Login as Customer (need to create one or use seeded one)
    # Seed script creates 'customer@bank.com' / 'customer123' usually? Let's check seed_db.py or create one.
    # Assuming seed_db creates a customer.
    session.post(login_url, data={'email': 'customer@bank.com', 'password': 'customer123'})
    resp = session.get('http://127.0.0.1:5001/calculator')
    if resp.status_code == 200:
        print("PASS: Customer Calculator Page")
    else:
        print(f"FAIL: Customer Calculator. Status: {resp.status_code}")

    # 3. Test Officer Filter
    print("\n--- Testing Officer Filter ---")
    session.post(login_url, data={'email': 'officer@bank.com', 'password': 'officer123'})
    resp = session.get('http://127.0.0.1:5001/officer/dashboard?status=Pending')
    if resp.status_code == 200:
        print("PASS: Officer Dashboard with Filter")
    else:
        print(f"FAIL: Officer Filter. Status: {resp.status_code}")

if __name__ == '__main__':
    # reset_db() # Run this carefully
    test_features()
