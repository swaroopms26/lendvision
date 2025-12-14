import requests

def test_login():
    session = requests.Session()
    
    # 1. Login
    login_url = 'http://127.0.0.1:5000/login'
    credentials = {'email': 'officer@bank.com', 'password': 'officer123'}
    
    print(f"Logging in to {login_url}...")
    response = session.post(login_url, data=credentials)
    print(f"Login Response: {response.status_code}")
    
    # 2. Access Dashboard
    dashboard_url = 'http://127.0.0.1:5000/officer/dashboard'
    print(f"Accessing {dashboard_url}...")
    response = session.get(dashboard_url)
    print(f"Dashboard Response: {response.status_code}")
    if response.status_code != 200:
        print("Content preview:")
        print(response.text[:200])

if __name__ == '__main__':
    test_login()
