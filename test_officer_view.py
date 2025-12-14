import requests

def test_officer_view():
    session = requests.Session()
    
    # Login
    login_url = 'http://127.0.0.1:5001/login'
    credentials = {'email': 'officer@bank.com', 'password': 'officer123'}
    session.post(login_url, data=credentials)
    
    # Access Application 1
    # Assuming app 1 exists (from previous context)
    app_url = 'http://127.0.0.1:5001/officer/application/1'
    print(f"Accessing {app_url}...")
    response = session.get(app_url)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Page loaded.")
    else:
        print("Failed.")
        print(response.text[:500])

if __name__ == '__main__':
    test_officer_view()
