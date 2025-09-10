#!/usr/bin/env python
"""
Simple test script to check public endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(url, name):
    """Test a specific endpoint"""
    print(f"\n🔍 Testing {name}: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS!")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Response: {response.text}")
        else:
            print("❌ FAILED!")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Test all public endpoints"""
    print("🚀 Testing Public Endpoints...")
    print("=" * 50)
    
    # Test public endpoints
    test_endpoint(f"{BASE_URL}/", "Home Page")
    test_endpoint(f"{BASE_URL}/api/status/", "API Status")
    test_endpoint(f"{BASE_URL}/api/test/", "Public Test")
    
    print("\n" + "=" * 50)
    print("🎉 Testing Complete!")
    print("\n📋 If you see 401 errors, it means you're trying to access a protected endpoint.")
    print("📋 Use the public endpoints above for testing without authentication.")

if __name__ == "__main__":
    main()





