#!/usr/bin/env python
"""
API Test Script for Cinemajoo
This script tests all API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_home_page():
    """Test the home page"""
    print("🏠 Testing Home Page...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Home page working!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Home page failed")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_status():
    """Test the API status endpoint"""
    print("\n📊 Testing API Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/status/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API status working!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ API status failed")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_registration():
    """Test user registration"""
    print("\n👤 Testing User Registration...")
    data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "testpass123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/register/", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Registration successful!")
            result = response.json()
            print(f"User: {result['user']['username']}")
            print(f"Access Token: {result['tokens']['access'][:50]}...")
            return result['tokens']['access']
        else:
            print("❌ Registration failed")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def test_login():
    """Test user login"""
    print("\n🔐 Testing User Login...")
    data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/login/", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login successful!")
            result = response.json()
            print(f"User: {result['user']['username']}")
            print(f"Access Token: {result['tokens']['access'][:50]}...")
            return result['tokens']['access']
        else:
            print("❌ Login failed")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def test_protected_endpoint(token):
    """Test a protected endpoint with token"""
    if not token:
        print("\n🔒 Skipping protected endpoint test (no token)")
        return
    
    print("\n🔒 Testing Protected Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/user-info/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Protected endpoint working!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Protected endpoint failed")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

def test_username_check():
    """Test username availability check"""
    print("\n🔍 Testing Username Check...")
    data = {"username": "newuser123"}
    try:
        response = requests.post(f"{BASE_URL}/api/check-username/", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Username check working!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ Username check failed")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Cinemajoo API Tests...")
    print("=" * 50)
    
    # Test public endpoints
    test_home_page()
    test_api_status()
    test_username_check()
    
    # Test authentication
    token = test_registration()
    if not token:
        token = test_login()
    
    # Test protected endpoints
    test_protected_endpoint(token)
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")

if __name__ == "__main__":
    main()


