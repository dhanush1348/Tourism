#!/usr/bin/env python
"""
Test script for Wanderlust API endpoints.
Run: python test_api.py
"""

import os
import json
import requests
import time
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = {
    "landing": "/",
    "chat": "/api/chat/",
    "bookings": "/api/bookings/",
    "health": "/health/",
    "destinations": "/destinations/",
    "packages": "/packages/",
}

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message."""
    print(f"✅ {text}")

def print_error(text):
    """Print error message."""
    print(f"❌ {text}")

def print_warning(text):
    """Print warning message."""
    print(f"⚠️  {text}")

def test_server_running():
    """Check if Django server is running."""
    print_header("1. Server Status Check")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print_success(f"Django development server is running at {BASE_URL}")
            return True
        else:
            print_error(f"Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to {BASE_URL}")
        print_error("Make sure Django server is running: python manage.py runserver")
        return False
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
        return False

def test_endpoints():
    """Test all endpoints."""
    print_header("2. Endpoint Status")
    
    results = {}
    for name, endpoint in ENDPOINTS.items():
        url = f"{BASE_URL}{endpoint}"
        try:
            if endpoint in ["/api/chat/", "/api/bookings/"]:
                # POST endpoints - these might return 400 without proper data
                response = requests.post(url, timeout=5)
            else:
                # GET endpoints
                response = requests.get(url, timeout=5)
            
            # 4xx responses mean the endpoint exists but request is invalid
            # which is fine for this test
            if response.status_code < 500:
                print_success(f"{name}: {endpoint} → {response.status_code}")
                results[name] = True
            else:
                print_error(f"{name}: {endpoint} → {response.status_code}")
                results[name] = False
        except Exception as e:
            print_error(f"{name}: {endpoint} → Error: {str(e)}")
            results[name] = False
    
    return results

def test_chat_api():
    """Test chat API endpoint."""
    print_header("3. Chat API Test")
    
    url = f"{BASE_URL}/api/chat/"
    payload = {
        "message": "Tell me a short fact about travel",
        "history": []
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "reply" in data:
                print_success("Chat API is working!")
                print(f"   Response: {data['reply'][:100]}...")
                return True
            else:
                print_error(f"Unexpected response format: {data}")
                return False
        elif response.status_code == 503:
            print_warning("Chat API: Service unavailable (GOOGLE_API_KEY not set)")
            print("   Action: Set GOOGLE_API_KEY in .env file")
            print("   Get key at: https://aistudio.google.com/app/apikey")
            return False
        else:
            print_error(f"Chat API returned {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print_warning("Chat API: Request timeout (might be API key issue or network)")
        return False
    except Exception as e:
        print_error(f"Chat API error: {str(e)}")
        return False

def test_booking_api():
    """Test booking API endpoint."""
    print_header("4. Booking API Test")
    
    url = f"{BASE_URL}/api/bookings/"
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "date": "2026-05-15",
        "guests": "2",
        "package_id": "1"
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("Booking API is working!")
                print(f"   Booking ID: {data.get('booking_id')}")
                print(f"   Total: ${data.get('total'):,}")
                return True
            else:
                print_error(f"Booking API error: {data.get('error')}")
                return False
        else:
            print_error(f"Booking API returned {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print_error(f"Booking API error: {str(e)}")
        return False

def check_env_file():
    """Check .env file configuration."""
    print_header("5. Environment Configuration")
    
    env_path = Path(".env")
    if not env_path.exists():
        print_error(".env file not found at root directory")
        return False
    
    print_success(".env file exists")
    
    # Check for GOOGLE_API_KEY
    with open(env_path, "r") as f:
        content = f.read()
        if "GOOGLE_API_KEY" in content:
            print_success("GOOGLE_API_KEY is configured")
            
            # Check if key is set
            if "AIzaSy" in content:
                print_success("API key appears to be set (starts with AIzaSy)")
                return True
            else:
                print_warning("API key is not set (still has placeholder)")
                print("   Action: Replace 'your-google-api-key-here' with your actual key")
                return False
        else:
            print_error("GOOGLE_API_KEY not found in .env")
            return False

def test_landing_page():
    """Test landing page rendering."""
    print_header("6. Landing Page Test")
    
    url = f"{BASE_URL}/"
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            if "Wanderlust" in response.text or "React" in response.text:
                print_success("Landing page is rendering")
                
                # Check for key React components
                checks = {
                    "Chat component": "chat" in response.text.lower(),
                    "Booking component": "booking" in response.text.lower(),
                    "Navigation": "navbar" in response.text.lower(),
                }
                
                for check_name, result in checks.items():
                    if result:
                        print_success(f"  → {check_name} found")
                    else:
                        print_warning(f"  → {check_name} not found")
                
                return True
            else:
                print_error("Landing page doesn't contain expected content")
                return False
        else:
            print_error(f"Landing page returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Landing page error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("\n" + "🚀 " * 30)
    print("WANDERLUST API TEST SUITE")
    print("🚀 " * 30)
    
    # Check if server is running first
    if not test_server_running():
        print_error("\n⛔ Cannot proceed. Start Django server first:")
        print("   python manage.py runserver")
        return
    
    # Run tests
    test_endpoints()
    test_landing_page()
    check_env_file()
    test_chat_api()
    test_booking_api()
    
    # Summary
    print_header("SUMMARY")
    print("""
✨ All tests completed!

Next steps:
1. If Chat API shows "Service unavailable":
   - Go to: https://aistudio.google.com/app/apikey
   - Create a new API key (no credit card needed for free tier)
   - Update .env file with: GOOGLE_API_KEY=AIzaSy...
   
2. Install Google Generative AI package:
   - pip install google-generativeai>=0.3.0
   
3. Restart Django server:
   - Press Ctrl+C in terminal
   - Run: python manage.py runserver
   
4. Test the chat:
   - Open http://127.0.0.1:8000/ in browser
   - Click the gold chat button (✦)
   - Ask Aria a question!

📚 Full setup guide: See GEMINI_SETUP.md
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
