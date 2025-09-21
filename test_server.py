#!/usr/bin/env python3
import requests
import time

# Wait for server to start
time.sleep(2)

try:
    response = requests.get("http://localhost:8000/")
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")