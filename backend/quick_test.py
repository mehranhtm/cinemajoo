#!/usr/bin/env python
"""
Quick test to verify server is running
"""

import requests

def test_server():
    """Test if server is responding"""
    try:
        print("🔍 Testing server...")
        response = requests.get("http://localhost:8000/api/test/", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is working!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Server returned error")
            print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        print("Please start the server with: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_server()

