#!/usr/bin/env python3
import requests
import json

# Test case search
data = {
    "state": "KARNATAKA",
    "commission": "Bangalore 1st & Rural Additional",
    "search_value": "123"
}

try:
    response = requests.post("http://localhost:8000/cases/by-case-number", json=data)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")