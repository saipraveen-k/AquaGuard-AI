#!/usr/bin/env python3
"""
Test web app API endpoints
"""

import requests
import json

def test_api():
    print("🔍 TESTING WEB APP API ENDPOINTS")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/flood-data",
        "/api/ship-data", 
        "/api/spill-data",
        "/api/alerts",
        "/api/kpi-summary",
        "/api/map-data"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   Success: {data.get('success', False)}")
                    if 'statistics' in data:
                        stats = data['statistics']
                        print(f"   Stats: {list(stats.keys())}")
                else:
                    print(f"   Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ {endpoint}: Connection error - {str(e)}")
        
        print()

if __name__ == '__main__':
    test_api()
