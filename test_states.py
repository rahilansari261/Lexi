#!/usr/bin/env python3
import requests
import time

# Wait for server to start
time.sleep(1)

try:
    response = requests.get("http://localhost:8000/states")
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")