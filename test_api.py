#!/usr/bin/env python3
"""
Test script for Jagriti Case Search API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:200]}...")
            return True
        else:
            print(f"❌ {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)}")
        return False

def main():
    print("🚀 Testing Jagriti Case Search API")
    print("=" * 50)
    
    # Test basic endpoints
    print("\n📋 Testing Basic Endpoints:")
    test_endpoint("GET", "/")
    test_endpoint("GET", "/states")
    test_endpoint("GET", "/commissions/1")
    
    # Test case search endpoints
    print("\n🔍 Testing Case Search Endpoints:")
    
    search_data = {
        "state": "KARNATAKA",
        "commission": "Bangalore 1st & Rural Additional",
        "search_value": "123"
    }
    
    endpoints = [
        "/cases/by-case-number",
        "/cases/by-complainant",
        "/cases/by-respondent",
        "/cases/by-complainant-advocate",
        "/cases/by-respondent-advocate",
        "/cases/by-industry-type",
        "/cases/by-judge"
    ]
    
    for endpoint in endpoints:
        test_endpoint("POST", endpoint, search_data)
    
    # Test error cases
    print("\n⚠️  Testing Error Cases:")
    test_endpoint("POST", "/cases/by-case-number", {}, 400)  # Missing data
    test_endpoint("POST", "/cases/by-case-number", {"state": "INVALID"}, 400)  # Invalid state
    test_endpoint("GET", "/commissions/999", {}, 200)  # Non-existent state ID
    
    print("\n✨ API Testing Complete!")

if __name__ == "__main__":
    main()