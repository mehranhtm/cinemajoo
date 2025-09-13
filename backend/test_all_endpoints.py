#!/usr/bin/env python
"""
Comprehensive test script for all Cinemajoo API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(url, method="GET", data=None, headers=None, name=None):
    """Test a specific endpoint"""
    if name is None:
        name = f"{method} {url}"
    
    print(f"\n🔍 Testing {name}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ SUCCESS!")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Response: {response.text}")
            return True
        else:
            print("❌ FAILED!")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Server might not be running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Test all endpoints"""
    print("🚀 Testing All Cinemajoo API Endpoints")
    print("=" * 60)
    
    # Test public endpoints
    print("\n📋 Testing Public Endpoints (No Authentication Required)")
    print("-" * 50)
    
    public_endpoints = [
        ("/", "GET", None, None, "Home Page"),
        ("/api/status/", "GET", None, None, "API Status"),
        ("/api/test/", "GET", None, None, "Public Test"),
    ]
    
    for url, method, data, headers, name in public_endpoints:
        test_endpoint(f"{BASE_URL}{url}", method, data, headers, name)
    
    # Test registration
    print("\n📋 Testing Registration")
    print("-" * 50)
    
    registration_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    test_endpoint(
        f"{BASE_URL}/api/register/",
        "POST",
        registration_data,
        {"Content-Type": "application/json"},
        "User Registration"
    )
    
    # Test login
    print("\n📋 Testing Login")
    print("-" * 50)
    
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    test_endpoint(
        f"{BASE_URL}/api/login/",
        "POST",
        login_data,
        {"Content-Type": "application/json"},
        "User Login"
    )
    
    # Test username check
    print("\n📋 Testing Username Check")
    print("-" * 50)
    
    username_data = {"username": "newuser123"}
    
    test_endpoint(
        f"{BASE_URL}/api/check-username/",
        "POST",
        username_data,
        {"Content-Type": "application/json"},
        "Username Availability Check"
    )
    
    print("\n" + "=" * 60)
    print("🎉 Testing Complete!")
    print("\n📋 Summary:")
    print("- Public endpoints should return 200 OK")
    print("- Registration should return 201 Created or 400 Bad Request")
    print("- Login should return 200 OK or 400 Bad Request")
    print("- Username check should return 200 OK")

if __name__ == "__main__":
    main()






