import requests

def test_login_flow():
    base_url = 'http://127.0.0.1:5001'
    s = requests.Session()
    
    print(f"1. GET {base_url}/login")
    r = s.get(f'{base_url}/login')
    print(f"   Status: {r.status_code}")
    
    print(f"2. POST {base_url}/login (Admin)")
    # allow_redirects=False to see the 302
    r = s.post(f'{base_url}/login', data={'email': 'admin@bank.com', 'password': 'admin123'}, allow_redirects=False)
    print(f"   Status: {r.status_code}")
    print(f"   Location: {r.headers.get('Location')}")
    
    if r.status_code == 302:
        next_url = r.headers['Location']
        # If relative, append to base
        if next_url.startswith('/'):
            next_url = base_url + next_url
            
        print(f"3. Following Redirect to {next_url} (should be GET)")
        r2 = s.get(next_url)
        print(f"   Status: {r2.status_code}")
        if r2.status_code == 405:
            print("   !!! DETECTED 405 METHOD NOT ALLOWED ON REDIRECT !!!")
            print("   Trying POST on redirect just to check...")
            r3 = s.post(next_url)
            print(f"   POST Status: {r3.status_code}")

    print("-" * 20)
    print(f"4. POST {base_url}/login (Officer)")
    r = s.post(f'{base_url}/login', data={'email': 'officer@bank.com', 'password': 'officer123'}, allow_redirects=False)
    print(f"   Status: {r.status_code}")
    print(f"   Location: {r.headers.get('Location')}")
    
    if r.status_code == 302:
        next_url = r.headers['Location']
        if next_url.startswith('/'):
            next_url = base_url + next_url
            
        print(f"5. Following Redirect to {next_url}")
        r2 = s.get(next_url)
        print(f"   Status: {r2.status_code}")

if __name__ == '__main__':
    try:
        test_login_flow()
    except Exception as e:
        print(f"Connection failed: {e}")
